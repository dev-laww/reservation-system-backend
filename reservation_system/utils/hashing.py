import bcrypt


def hash_password(password: str) -> str:
    """
    Hash password.

    :param password: password.
    :return: hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    """
    Check password.

    :param password: password.
    :param hashed_password: hashed password.
    :return: True if password is correct, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
