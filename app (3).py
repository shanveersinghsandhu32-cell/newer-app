import os, json
import streamlit as st
from web3 import Web3
from eth_account import Account
from utils import sha256_file_bytes, sha256_file_to_bytes32

RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:8545")
CONTRACT_JSON = "deployed_contract.json"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not os.path.exists(CONTRACT_JSON):
    st.error("Run deploy.py first.")
    st.stop()

with open(CONTRACT_JSON) as f:
    info = json.load(f)
contract = w3.eth.contract(address=info["address"], abi=info["abi"])

st.title("Blockchain Certificate Registry")

menu = st.sidebar.selectbox("Menu", ["Issue", "Verify", "Admin"])

def sign_and_send(tx, priv):
    acct = Account.from_key(priv)
    tx["nonce"] = w3.eth.get_transaction_count(acct.address)
    tx["gasPrice"] = w3.eth.gas_price
    signed = acct.sign_transaction(tx)
    h = w3.eth.send_raw_transaction(signed.rawTransaction)
    rc = w3.eth.wait_for_transaction_receipt(h)
    return h.hex(), rc

if menu == "Issue":
    priv = st.text_input("Issuer private key", type="password")
    meta = st.text_input("Metadata URI")
    file = st.file_uploader("Upload certificate", type=["pdf","png","jpg","jpeg"])
    if st.button("Issue") and priv and file:
        data = file.read()
        h = sha256_file_bytes(data)
        st.write("SHA-256:", h)
        cert_b = sha256_file_to_bytes32(data)
        acct = Account.from_key(priv).address
        txn = contract.functions.issueCertificate(cert_b, meta).build_transaction({"from": acct, "gas":200000})
        try:
            txh, _ = sign_and_send(txn, priv)
            st.success("Issued, tx: "+txh)
        except Exception as e:
            st.error(e)

if menu == "Verify":
    file = st.file_uploader("Upload cert", type=["pdf","png","jpg","jpeg"])
    if st.button("Verify") and file:
        data = file.read()
        h = sha256_file_bytes(data)
        cert_b = sha256_file_to_bytes32(data)
        st.write("SHA-256:", h)
        c = contract.functions.getCertificate(cert_b).call()
        if c[1] == "0x0000000000000000000000000000000000000000":
            st.error("Not found")
        elif c[4]:
            st.error("Revoked")
        else:
            st.success("Valid certificate")
            st.json({"issuer": c[1], "issueDate": c[2], "metadataURI": c[3]})

if menu == "Admin":
    priv = st.text_input("Owner private key", type="password")
    addr = st.text_input("Issuer address")
    allow = st.checkbox("Allow issuer?")
    if st.button("Set issuer") and priv and addr:
        acct = Account.from_key(priv).address
        txn = contract.functions.setIssuer(addr, allow).build_transaction({"from": acct,"gas":100000})
        txh, _ = sign_and_send(txn, priv)
        st.success("Tx: "+txh)
