from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class AESManager:
    @staticmethod
    def encrypt(plain_msg: str, key: bytes) -> bytes:
        return AES.new(key, AES.MODE_ECB).encrypt(pad(plain_msg.encode(), AES.block_size))
    
    @staticmethod
    def decrypt(encrypted_msg: str, key: bytes) -> bytes:
        return unpad(AES.new(key, AES.MODE_ECB).decrypt(encrypted_msg), AES.block_size).decode()
    
    