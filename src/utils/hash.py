import bcrypt


def hash_password(value: str) -> str:
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()


def check_hash(hashed_value: str, value: str) -> bool:
    return bcrypt.checkpw(value.encode(), hashed_value.encode())
