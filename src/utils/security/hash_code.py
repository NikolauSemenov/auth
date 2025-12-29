from cryptography.fernet import Fernet

from src.config.settings import settings

fernet = Fernet(settings.email_secret_code)


def encrypt_code(code: str) -> str:
    return fernet.encrypt(code.encode()).decode()


def decrypt_code(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
