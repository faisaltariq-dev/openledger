1-bash:
python3 -m venv .env && source .env/bin/activate && python -m pip install -r requirements.txt

2-software architucture:
openledger/
│
├── generator.py
├── sender.py
├── miner.py
├── ledger.json#chain storage
└── readme.txt

