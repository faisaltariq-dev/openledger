Openledger: a fun simulation of how cryptocurrencies work

your keys never leave your machine you as a client the you run a python script that only broadcasts the signed transaction and the server legitmizes your request through sha-256 and appends it to the public ledger once confirmed, THE SERVER NEVER SEES THE KEYS

cryptocurrency operates on self-custody and decentralization,hence:
1-everybody gets access to the public ledger at any time
2-no personal information connects any crypto holder to the address which holds the crypto, only keys matter make the crypto yours

how to use: run holder.py anywhere. as can be seen in the demo video google colab works fine. Once deployed on PythonAnywhere as a live demo (now retired).

limitations:
1-the algorithm does not create new tokens for miners
2-hashing is not done on blockchain-level rather just experiemental

usage is easy for the client no dependencies no dragging trnasaction jsons
example usage:
python holder.py        # option 1 -> generate a wallet
python holder.py        # option 2 -> check the Nakamoto balance (50)
python holder.py        # option 3 -> build a transaction (produces tx_<id>.json)
hint: the keys for the original 50 nakamotocoins is a comment in the code! 

Repo layout
openledger/
├── holder.py        # client: wallet gen, balance, transaction signing
├── chain.py         # server: verification + block appending
├── ledger.json      # the chain (ships with a genesis block)
├── requirements.txt # the requirements of the backend
├── demo_openledger.mp4      # 65 second video demo on google colab
├── README.md
└── v1/              # earlier iteration (see below)
v1/ — the earlier design
v1/ keeps the first working iteration around to show how the design got simpler over time. In that version the client persisted a wallet JSON and every transaction lived as its own separate file. The final design distilled all of that down to the clean three-option client you see above — generate, check, sign — while holding the same core principle throughout: all math is local, and no key ever leaves the holder's machine.




How it works
holder.py (client side)
Run it and pick one of three options:

1-Generate wallet — needs nothing. Creates a private key (secrets.token_hex(32)) and derives the public key as its SHA-256 hash. Saves to wallet_<id>.json.
2-Check balance — needs only a public key so anyone can see the balance of all and of any public addresses. Replays the ledger and sums incoming minus outgoing.
3-Create transaction — needs both keys public and private(never leaves local). Builds the transaction, hashes it, "signs" it, and writes a tx_<id>.json file ready to hand to the server.

if the server's math check passes. The chain.py on the backend wraps the transaction in a block with the previous block's hash, hashes the whole block, and appends it to ledger.json. That previous_hash link is what makes the chain a chain 
hintt:The ledger ships with a genesis block granting 50 coins to a "Nakamoto" wallet, so there's something in the system to actually spend.

PythonAnywhere Setup (OpenLedger Backend)
1. Logged into pythonanywhere.com  
2. Web tab → Add new web app  
3. Manual configuration → Python 3.11  
Opened Bash console:
4. Cloned the private backend repository  
   (files used: `chain.py`, `ledger.json`, `requirements.txt`)  
5. Installed dependencies:(flask)
   pip3.11 install --user -r requirements.txt
Edited WSGI file:
6. Set application path to the project directory and imported:
from chain import app as application
Reloaded the web app.
Backend live at:
https://forkcommit.pythonanywhere.com
The json data at:
https://forkcommit.pythonanywhere.com/ledger

Originally built and deployed under my personal dev account; mirrored here for portfolio purposes