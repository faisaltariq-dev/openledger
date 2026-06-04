import secrets
import hashlib
import json

def generate_keys():
    private_key = secrets.token_hex(32)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()

    wallet = {
        "private_key": private_key,
        "public_key": public_key
    }

    with open("wallet.json", "w") as f:
        json.dump(wallet, f, indent=4)

    print("Wallet generated successfully.")
    print("Public Key:", public_key)

if __name__ == "__main__":
    generate_keys()