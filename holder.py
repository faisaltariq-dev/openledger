import hashlib
import secrets
import json
import time
import uuid
import urllib.request
import urllib.error

BACKEND_URL = "https://forkcommit.pythonanywhere.com"

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

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

    tx_string = json.dumps(transaction, sort_keys=True)
    tx_hash = sha256(tx_string)
    signature = sha256(public_key + tx_hash)

    transaction["tx_hash"] = tx_hash
    transaction["signature"] = signature

    payload = json.dumps(transaction).encode("utf-8")
    req = urllib.request.Request(
        f"{BACKEND_URL}/submit",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            print("Transaction accepted.")
            print("Block index:", result["block_index"])
            print("Block hash:", result["block_hash"])
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        print("Transaction rejected:", body.get("message", "Unknown error"))
    except urllib.error.URLError as e:
        print("Network error:", e.reason)

def check_balance():
    public_key = input("Enter your public key: ").strip()

    url = f"{BACKEND_URL}/balance/{public_key}"
    req = urllib.request.Request(url, method="GET")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            print("Public key:", result["public_key"])
            print("Balance:", result["balance"])
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        print("Error:", body.get("message", "Unknown error"))
    except urllib.error.URLError as e:
        print("Network error:", e.reason)

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