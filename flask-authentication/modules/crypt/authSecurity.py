import base64, hashlib

from .aesManager import AESManager
from .rsaManager import RSAManager

class AuthSecurity:
    @staticmethod
    def defaultEncrypt(plain_msg: str, key: bytes) -> str:
        return base64.b64encode(AESManager.encrypt(plain_msg, key)).decode()
    
    @staticmethod
    def defaultDecrypt(encrypted_msg: str, key: bytes) -> str:
        return AESManager.decrypt(base64.b64decode(encrypted_msg), key)
    
    @staticmethod
    def passwordEncrypt(user_pwd: str) -> str:
        s = hashlib.sha256()
        s.update(user_pwd.encode())
        return s.hexdigest()