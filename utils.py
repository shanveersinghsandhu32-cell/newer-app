import hashlib
from web3 import Web3

def sha256_file_bytes(file_bytes: bytes) -> str:
    h = hashlib.sha256()
    h.update(file_bytes)
    return h.hexdigest()

def sha256_file_to_bytes32(file_bytes: bytes) -> bytes:
    hex_digest = sha256_file_bytes(file_bytes)
    return Web3.toBytes(hexstr=hex_digest)

def hex_to_bytes32(hexstr: str) -> bytes:
    if hexstr.startswith("0x"):
        hexstr = hexstr[2:]
    return Web3.toBytes(hexstr=hexstr)
