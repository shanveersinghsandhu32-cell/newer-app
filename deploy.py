import os
from solcx import install_solc, compile_standard
import json
from web3 import Web3
from eth_account import Account

RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:8545")
DEPLOYER_PRIVATE_KEY = os.getenv("DEPLOYER_PRIVATE_KEY")

if DEPLOYER_PRIVATE_KEY is None:
    raise SystemExit("set DEPLOYER_PRIVATE_KEY in env")

install_solc("0.8.17")
with open("contracts/CertificateRegistry.sol", "r") as f:
    source = f.read()

compiled = compile_standard({
    "language": "Solidity",
    "sources": {"CertificateRegistry.sol": {"content": source}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode.object"]}}}
}, solc_version="0.8.17")

abi = compiled["contracts"]["CertificateRegistry.sol"]["CertificateRegistry"]["abi"]
bytecode = compiled["contracts"]["CertificateRegistry.sol"]["CertificateRegistry"]["evm"]["bytecode"]["object"]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = Account.from_key(DEPLOYER_PRIVATE_KEY)

Certificate = w3.eth.contract(abi=abi, bytecode=bytecode)
construct_txn = Certificate.constructor().build_transaction({
    "from": acct.address,
    "nonce": w3.eth.get_transaction_count(acct.address),
    "gas": 5000000,
    "gasPrice": w3.eth.gas_price
})

signed = acct.sign_transaction(construct_txn)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print("Deploying... tx:", tx_hash.hex())
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed at:", tx_receipt.contractAddress)

with open("deployed_contract.json", "w") as f:
    json.dump({"address": tx_receipt.contractAddress, "abi": abi}, f, indent=2)
