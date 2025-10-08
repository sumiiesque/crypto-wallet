import hashlib
from ecdsa import SigningKey, SECP256k1, util
import base58

def sign_message(private_key: bytes, message: str) -> str:
    """Sign a message with a private key"""
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    message_hash = hashlib.sha256(message.encode()).digest()
    signature = sk.sign_digest(message_hash, sigencode=util.sigencode_string)
    return signature.hex()

def to_wif(private_key: bytes) -> str:
    """Convert private key to Bitcoin WIF format"""
    extended = b'\x80' + private_key
    extended += b'\x01'  # compression flag
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()
