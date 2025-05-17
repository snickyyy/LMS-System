from cryptography.fernet import Fernet

from settings.settings import get_settings

fernet = Fernet(f'{get_settings().APP.SECRET_KEY}')

def encrypt(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    return fernet.decrypt(data.encode()).decode()
