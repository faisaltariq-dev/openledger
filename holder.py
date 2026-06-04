import hashlib
import secrets
import json
import time
import uuid

#print("must create a wallet before so you dont burn the only 50btc in the system")
#print("hint: the public key to nakamoto of balance 50 is:")
#print("52a7066d73950870109c258f28811c52446c82433aaad7327441ab199b5b6de3")
#print("hint: the private key to nakamoto of balance 50 is:")
#print("7005c2fe1766f02e311d02c01939d29c7ea2e24e9ef155b5eed2fd75cd44ffa0")


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


# ---------------------------
# WALLET GENERATION
# ---------------------------

def generate_wallet():
    private_key = secrets.token_hex(32)
    public_key = sha256(private_key)

    wallet = {
        "private_key": private_key,
        "public_key": public_key
    }

    filename = f"wallet_{public_key[:8]}.json"
    with open(filename, "w") as f:
        json.dump(wallet, f, indent=4)

    print("Wallet generated.")
    print("Public key:", public_key)
    print("Saved as:", filename)


# ---------------------------
# TRANSACTION CREATION
# ---------------------------

def create_transaction():
    private_key = input("Enter your private key: ").strip()
    public_key = sha256(private_key)

    receiver = input("Receiver public key: ").strip()
    amount = input("Amount: ").strip()

    transaction = {
        "sender": public_key,
        "receiver": receiver,
        "amount": amount,
        "timestamp": time.time(),
        "tx_id": str(uuid.uuid4())
    }

    # Create transaction hash (without signature)
    tx_string = json.dumps(transaction, sort_keys=True)
    tx_hash = sha256(tx_string)

    # Signature (educational model)
    signature = sha256(public_key + tx_hash)

    transaction["tx_hash"] = tx_hash
    transaction["signature"] = signature

    filename = f"tx_{transaction['tx_id']}.json"
    with open(filename, "w") as f:
        json.dump(transaction, f, indent=4)

    print("Transaction created.")
    print("Saved as:", filename)

#
#
#
def check_balance():
    import os

    public_key = input("Enter your public key: ").strip()

    if not os.path.exists("ledger.json"):
        print("No ledger found. Balance = 0")
        return

    with open("ledger.json") as f:
        chain = json.load(f)

    balance = 0.0

    for block in chain:
        tx = block["transaction"]

        if tx["receiver"] == public_key:
            balance += float(tx["amount"])

        if tx["sender"] == public_key:
            balance -= float(tx["amount"])

    print("Public key:", public_key)
    print("Balance:", balance)
# ---------------------------
# MENU
# ---------------------------

if __name__ == "__main__":
    print("1. Generate wallet")
    print("2. Create transaction")
    print("3. Check balance")
    choice = input("Select option: ").strip()
    

    if choice == "1":
        generate_wallet()
    elif choice == "2":
        create_transaction()
    elif choice == "3":
        check_balance()