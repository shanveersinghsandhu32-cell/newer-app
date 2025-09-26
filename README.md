# Blockchain Certificate System

A tamper-proof system for issuing, storing, and verifying student certificates on blockchain.  
Built with **Solidity**, **Python (web3.py)**, and **Streamlit**.

---

## Features
- ✅ Certificates issued by authorized issuers
- ✅ SHA-256 file hash stored on-chain for tamper-proof verification
- ✅ Admin can authorize issuers or revoke certificates
- ✅ Simple Streamlit web interface for issuing and verifying

---

## Project Structure
```
contracts/CertificateRegistry.sol   # Solidity smart contract
deploy.py                           # Deploy contract to Ethereum/Ganache
utils.py                            # Python helpers (hashing, etc.)
app.py                              # Streamlit frontend
requirements.txt                    # Dependencies
```

---

## Setup Instructions

### 1. Clone repo & install dependencies
```bash
git clone <your-repo-url>
cd blockchain_certificate_system
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start local blockchain
You can use [Ganache](https://trufflesuite.com/ganache/) or Hardhat.

Ganache example:
```bash
ganache-cli --deterministic
```

### 3. Deploy contract
Export a private key from Ganache (one of the provided test accounts):

```bash
export DEPLOYER_PRIVATE_KEY=0x<your_private_key>
export RPC_URL=http://127.0.0.1:8545
python deploy.py
```

This creates `deployed_contract.json` with contract address & ABI.

### 4. Run Streamlit app
```bash
streamlit run app.py
```

Open in browser: [http://localhost:8501](http://localhost:8501)

---

## Usage

### Admin
- Use **Admin tab** to authorize an issuer’s address.  
- Owner (the deployer) controls this.

### Issuer
- Switch to **Issue tab**
- Enter private key (for demo only)
- Upload certificate file (PDF/JPG/PNG)
- Certificate is hashed (SHA-256) and stored on-chain.

### Verify
- Upload certificate file or paste SHA-256 hash
- App checks blockchain and displays validity.

---

## Security Notes
- Private keys are entered in UI for demo only.  
  ⚠️ In production, never expose raw private keys. Use MetaMask, WalletConnect, or a secure backend.
- Consider IPFS for storing full certificate files and only keeping the hash on-chain.

---

## License
MIT
