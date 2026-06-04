import json
import hashlib
import time
import uuid

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def create_transaction():
    with open("wallet.json") as f:
        wallet = json.load(f)

    sender = wallet["public_key"]
    private_key = wallet["private_key"]

    receiver = input("Receiver public key: ")
    amount = input("Amount: ")

    transaction = {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": time.time(),
        "tx_id": str(uuid.uuid4())
    }

    tx_string = json.dumps(transaction, sort_keys=True)
    tx_hash = sha256(tx_string)

    signature = sha256(sender + tx_hash)
    transaction["signature"] = signature

    with open("transaction.json", "w") as f:
        json.dump(transaction, f, indent=4)

    print("Transaction created and signed.")

if __name__ == "__main__":
    create_transaction()