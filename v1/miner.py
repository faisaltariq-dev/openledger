import json
import hashlib
import time

DIFFICULTY_PREFIX = "0000"

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def verify_transaction(tx):
    signature = tx.pop("signature")
    tx_string = json.dumps(tx, sort_keys=True)
    tx_hash = sha256(tx_string)

    expected_signature = sha256(tx["sender"] + tx_hash)

    tx["signature"] = signature
    return signature == expected_signature

def mine_block(transaction):
    try:
        with open("ledger.json") as f:
            chain = json.load(f)
    except FileNotFoundError:
        chain = []

    previous_hash = chain[-1]["hash"] if chain else "0"

    block = {
        "index": len(chain) + 1,
        "previous_hash": previous_hash,
        "timestamp": time.time(),
        "transaction": transaction,
        "nonce": 0
    }

    while True:
        block_string = json.dumps(block, sort_keys=True)
        block_hash = sha256(block_string)

        if block_hash.startswith(DIFFICULTY_PREFIX):
            block["hash"] = block_hash
            break

        block["nonce"] += 1

    chain.append(block)

    with open("ledger.json", "w") as f:
        json.dump(chain, f, indent=4)

    print("Block mined successfully.")
    print("Hash:", block_hash)

if __name__ == "__main__":
    with open("transaction.json") as f:
        transaction = json.load(f)

    if verify_transaction(transaction):
        print("Transaction verified.")
        mine_block(transaction)
    else:
        print("Invalid transaction. Mining aborted.")