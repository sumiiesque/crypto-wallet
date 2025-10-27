import hashlib
import base58

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def ripemd160(data: bytes) -> bytes:
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.digest()

def generate_bitcoin_address(public_key: bytes) -> str:
    """Generate Bitcoin address from public key"""
    hash160 = ripemd160(sha256(public_key))
    versioned = b'\x00' + hash160
    checksum = sha256(sha256(versioned))[:4]
    return base58.b58encode(versioned + checksum).decode()

def generate_ethereum_address(public_key: bytes) -> str:
    """Generate Ethereum address from public key"""
    pub_key_no_prefix = public_key[1:]
    keccak_hash = hashlib.sha3_256(pub_key_no_prefix).digest()
    return "0x" + keccak_hash[-20:].hex()
