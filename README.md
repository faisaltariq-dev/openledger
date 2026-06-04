# Openledger: a fun simulation of how cryptocurrencies work

your keys never leave your machine you as a client the you run a python script that only broadcasts the signed transaction and the server legitmizes your request through sha-256 and appends it to the public ledger once confirmed, THE SERVER NEVER SEES THE KEYS

cryptocurrency operates on self-custody and decentralization,hence:

1-everybody gets access to the public ledger at any time
2-anybody can send a transaction request to the chain at any time
3-no personal information connects any crypto holder to the address which holds the crypto, only keys matter make the crypto yours

how to use: run holder.py which requires no dependencies. 

## limitations:

1-the algorithm does not create new cryptocurrency tokens for miners

2-hashing is not done on blockchain-level rather just experiemental

## possible improvments:
1-have the nakamoto wallet receive 2 coins with every sucessful transaction

2- improve encryption,server-client traffic,etc


## usage is easy for the client no dependencies no manually plugging transaction jsons 
# CHECK OUT 65 SECOND VIDEO

### example usage:
#### hintt:The ledger ships with a genesis block granting 50 coins to a "Nakamoto" wallet, so there's something in the system to actually spend.
python holder.py        # option 1 -> generate a wallet and a wallaet json which holds the private key
```
Select option: 1
Wallet generated.
Public key: c734fe646dbc8b167f91322a9810fdbeec5c260ba6a519a7f95b9a3f4e88aca8
Saved as: wallet_531199b4.json
```
python holder.py        # option 2 -> redeem the Nakamoto balance (50) by building a transaction api call with the transaction info and tells the user holder if he got accepted or rejected
```
Select option: 2
Enter your private key: 7005c2fe1766f02e311d02c01939d29c7ea2e24e9ef155b5eed2fd75cd44ffa0
Receiver public key: c734fe646dbc8b167f91322a9810fdbeec5c260ba6a519a7f95b9a3f4e88aca8
Amount: 48
Transaction accepted.
Block index: 2
Block hash: 998667017209d790f3085e0a6aecaeff2a221c7bed82f1cedbfa763cb59b7d6e
```
python holder.py        # option 3 -> check the balance of the new wallet
```
Select option: 3
Enter your public key: c734fe646dbc8b167f91322a9810fdbeec5c260ba6a519a7f95b9a3f4e88aca8
Public key: c734fe646dbc8b167f91322a9810fdbeec5c260ba6a519a7f95b9a3f4e88aca8
Balance: 48
```

## Repo layout

openledger/
├── holder.py        # client: wallet gen, balance, transaction requests to server
├── chain.py         # server: receives requests + verification + block appending
├── ledger.json      # the chain (ships with a genesis block)
├── requirments.txt  # the requirements of the backend
├── demo_openledger.mp4      # 65 second video demo on google colab
├── README.md
└── v1/              # earlier iteration (see below)


### v1/ — the earlier design

v1/ keeps the first working iteration around to show how the design got simpler over time. In that version the client persisted a wallet JSON and every transaction lived as its own separate file. The final design distilled all of that down to the clean three-option client you see above — generate, check, sign — while holding the same core principle throughout: all math is local, and no key ever leaves the holder's machine.








## How it works

### holder.py (client side)

Run it and pick one of three options:

holder.py simulates modern cryptowallets, which literally do 3 things only: generate a wallet upon an agreed algorithm, broadcast transaction requests with signed hashes instead of actual keys and finally it inquires upon any public address including itselg!

option1-Generate wallet: needs nothing. Creates a private key (secrets.token_hex(32)) and derives the public key as its SHA-256 hash. saves it as wallet_<id>.json.

option2-Create transaction: needs both keys public and private(never leaves local). Builds the transaction, hashes it, "signs" it, and POSTs it to the server.

option3-Check balance: needs only a public key so anyone can see the balance of all and of any public addresses. Asks the server, which sums incoming minus outgoing.

### chain.py (server side)

if the server's math check passes. The chain.py on the backend wraps the transaction in a block with the previous block's hash, hashes the whole block, and appends it to ledger.json. That previous_hash link is what makes the chain a chain

option1-wallet generation: the server does absolutely nothing here, the decentralized nature of cryptocurrency dictates that no permission from the chain is needed by anyone in order to generate a wallet

option2-receive transaction: the server receives the post submit, process the requests with the appropriate cryptography mathmattics and either rejects or acceepts and appends to the ledger json

option3- ledger checks: the server receives the get requesst from the client and responds back with the balance of any public wallet as per cryptocurrency publicity policy

Endpoints:
```
GET  /                      explorer page
POST /submit                submit a signed transaction
GET  /balance/<public_key>  check a balance
GET  /ledger                full chain as JSON
```
## PythonAnywhere Setup (OpenLedger Backend)

1. Logged into pythonanywhere.com
2. Web tab → Add new web app
3. Manual configuration → Python 3.11

Opened Bash console:

4. Cloned the private backend repository
   (files used: `chain.py`, `ledger.json`, `requirements.txt`)
5. Installed dependencies:(flask)

```
pip3.11 install --user -r requirements.txt
```

Edited WSGI file to configure the web application:

6. Set application path to the project directory and imported:

```
from chain import app as application
```

Reloaded the web app.

Backend live at:
https://forkcommit.pythonanywhere.com

The json data at:
https://forkcommit.pythonanywhere.com/ledger

Originally built and deployed under my personal dev account; mirrored here for portfolio purposes
