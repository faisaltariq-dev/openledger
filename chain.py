import json
import hashlib
import time
import os


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


def verify_transaction(tx):
    chain = load_ledger()

    signature = tx["signature"]
    provided_tx_hash = tx["tx_hash"]

    # rebuild transaction WITHOUT tx_hash and signature
    tx_copy = tx.copy()
    del tx_copy["signature"]
    del tx_copy["tx_hash"]

    tx_string = json.dumps(tx_copy, sort_keys=True)
    recomputed_hash = sha256(tx_string)

    # 1️⃣ Integrity check
    if recomputed_hash != provided_tx_hash:
        print("Transaction hash mismatch.")
        return False

    # 2️⃣ Signature check
    expected_signature = sha256(tx["sender"] + recomputed_hash)

    if expected_signature != signature:
        print("Invalid signature.")
        return False

    # 3️⃣ Balance check
    sender_balance = compute_balance(tx["sender"], chain)

    if float(tx["amount"]) > sender_balance:
        print("Insufficient balance.")
        return False

    return True

def compute_balance(public_key, chain):
    balance = 0.0

    for block in chain:
        tx = block["transaction"]

        if tx["receiver"] == public_key:
            balance += float(tx["amount"])

        if tx["sender"] == public_key:
            balance -= float(tx["amount"])

    return balance

def append_block(tx):
    chain = load_ledger()
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

    print("Block appended.")
    print("Block hash:", block_hash)


if __name__ == "__main__":
    filename = input("Enter transaction file name:(with extension) ").strip()

    with open(filename) as f:
        tx = json.load(f)

    if verify_transaction(tx):
        print("Transaction valid.")
        append_block(tx)
    else:
        print("Transaction rejected.")