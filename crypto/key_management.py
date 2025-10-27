import os
from ecdsa import SigningKey, SECP256k1

class KeyManagement:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_private_key(self):
        """Generate random 32-byte private key"""
        self.private_key = os.urandom(32)
        return self.private_key

    def import_private_key(self, hex_key):
        """Import private key from hex string"""
        self.private_key = bytes.fromhex(hex_key)
        self.derive_public_key()

    def derive_public_key(self):
        """Derive uncompressed public key"""
        if not self.private_key:
            raise ValueError("Private key missing")
        sk = SigningKey.from_string(self.private_key, curve=SECP256k1)
        self.public_key = b'\x04' + sk.get_verifying_key().to_string()
        return self.public_key
