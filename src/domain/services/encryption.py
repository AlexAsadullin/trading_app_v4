import base64
import hashlib

from cryptography.fernet import Fernet

from config import settings


_fernet = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        secret = settings.secret_key.get_secret_value()
        key = base64.urlsafe_b64encode(hashlib.sha256(secret.encode()).digest())
        _fernet = Fernet(key)
    return _fernet


def encrypt_token(token: str) -> str:
    return _get_fernet().encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    return _get_fernet().decrypt(encrypted_token.encode()).decode()
