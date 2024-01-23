import sys
import crypto
sys.modules['Crypto'] = crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode

class RSAManager:
    @staticmethod
    def init() -> tuple[bytes, bytes]:
        key = RSA.generate(1024)
        return key.export_key(), key.public_key().export_key()

    @staticmethod
    def encrypt(plain_msg: str, public_key: str) -> str:
        return PKCS1_OAEP.new(RSA.import_key(public_key)).encrypt(plain_msg.encode())
    
    @staticmethod
    def decrypt(encrypted_msg: str, private_key: str) -> str:
        return PKCS1_OAEP.new(RSA.import_key(private_key), hashAlgo=SHA256).decrypt(b64decode(encrypted_msg)).decode()
