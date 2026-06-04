import json
import hashlib
import time
import os
import threading

from flask import Flask, request, jsonify

_ledger_lock = threading.Lock()
app = Flask(__name__)


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def load_ledger():
    if not os.path.exists("ledger.json"):
        return []
    with open("ledger.json") as f:
        return json.load(f)


def save_ledger(chain):
    with open("ledger.json", "w") as f:
        json.dump(chain, f, indent=4)


def verify_transaction(tx, chain):
    signature = tx.get("signature")
    provided_tx_hash = tx.get("tx_hash")

    # rebuild transaction WITHOUT tx_hash and signature
    tx_copy = tx.copy()
    tx_copy.pop("signature", None)
    tx_copy.pop("tx_hash", None)

    tx_string = json.dumps(tx_copy, sort_keys=True)
    recomputed_hash = sha256(tx_string)

    # 1. Integrity check
    if recomputed_hash != provided_tx_hash:
        return False, "Transaction hash mismatch"

    # 2. Signature check
    expected_signature = sha256(tx["sender"] + recomputed_hash)
    if expected_signature != signature:
        return False, "Invalid signature"

    # 3. Balance check
    sender_balance = compute_balance(tx["sender"], chain)
    if float(tx["amount"]) > sender_balance:
        return False, "Insufficient balance"

    return True, "OK"


def compute_balance(public_key, chain):
    balance = 0.0
    for block in chain:
        tx = block["transaction"]
        if tx["receiver"] == public_key:
            balance += float(tx["amount"])
        if tx["sender"] == public_key:
            balance -= float(tx["amount"])
    return balance


def append_block(tx, chain):
    previous_hash = chain[-1]["block_hash"] if chain else "0"

    block = {
        "index": len(chain) + 1,
        "previous_hash": previous_hash,
        "timestamp": time.time(),
        "transaction": tx,
    }

    block_string = json.dumps(block, sort_keys=True)
    block_hash = sha256(block_string)
    block["block_hash"] = block_hash
    chain.append(block)

    save_ledger(chain)
    return block


def _seed_ledger_if_needed():
    if not os.path.exists("ledger.json"):
        repo_ledger = os.path.join(os.path.dirname(__file__), "ledger.json")
        if os.path.exists(repo_ledger):
            with open(repo_ledger) as f:
                genesis = json.load(f)
            save_ledger(genesis)

_seed_ledger_if_needed()


REQUIRED_TX_FIELDS = {"sender", "receiver", "amount", "timestamp", "tx_id", "tx_hash", "signature"}

_EXPLORER_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>OpenLedger Explorer</title>
<style>
  body {{ background: #0d0d0d; color: #c8c8c8; font-family: monospace; padding: 2rem; }}
  h1 {{ color: #7fff7f; margin-bottom: 1.5rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th {{ background: #1a1a1a; color: #7fff7f; padding: 0.6rem 1rem; text-align: left; border-bottom: 1px solid #333; }}
  td {{ padding: 0.5rem 1rem; border-bottom: 1px solid #222; font-size: 0.85rem; word-break: break-all; }}
  tr:hover td {{ background: #151515; }}
  .hash {{ color: #5599ff; }}
  .amount {{ color: #ffcc44; }}
</style>
</head>
<body>
<h1>OpenLedger Explorer</h1>
<p>{block_count} block(s) on chain.</p>
<table>
<tr>
  <th>#</th><th>Timestamp</th><th>Sender</th><th>Receiver</th><th>Amount</th><th>Block Hash</th>
</tr>
{rows}
</table>
</body>
</html>"""

_ROW_TEMPLATE = """<tr>
  <td>{index}</td>
  <td>{timestamp}</td>
  <td class="hash">{sender}</td>
  <td class="hash">{receiver}</td>
  <td class="amount">{amount}</td>
  <td class="hash">{block_hash}</td>
</tr>"""


@app.route("/submit", methods=["POST"])
def submit():
    tx = request.get_json(silent=True)
    if not tx:
        return jsonify(status="error", message="Invalid or missing JSON body"), 400

    missing = REQUIRED_TX_FIELDS - tx.keys()
    if missing:
        return jsonify(status="error", message=f"Missing fields: {sorted(missing)}"), 400

    with _ledger_lock:
        chain = load_ledger()
        valid, reason = verify_transaction(tx, chain)
        if not valid:
            return jsonify(status="rejected", message=reason), 422
        block = append_block(tx, chain)

    return jsonify(status="accepted", block_index=block["index"], block_hash=block["block_hash"]), 201


@app.route("/balance/<public_key>", methods=["GET"])
def balance(public_key):
    chain = load_ledger()
    bal = compute_balance(public_key, chain)
    return jsonify(public_key=public_key, balance=bal), 200


@app.route("/ledger", methods=["GET"])
def ledger():
    chain = load_ledger()
    return jsonify(chain), 200


@app.route("/", methods=["GET"])
def explorer():
    chain = load_ledger()
    rows = []
    for block in chain:
        tx = block["transaction"]
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(block.get("timestamp", 0)))
        rows.append(_ROW_TEMPLATE.format(
            index=block["index"],
            timestamp=ts,
            sender=tx["sender"],
            receiver=tx["receiver"],
            amount=tx["amount"],
            block_hash=block["block_hash"],
        ))
    html = _EXPLORER_HTML.format(block_count=len(chain), rows="\n".join(rows))
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)