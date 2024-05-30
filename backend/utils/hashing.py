import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    :param password: The password to hash.
    :return: The hashed password as a string.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    # Return the hashed password as a string
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    :param plain_password: The plain text password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the password matches, False otherwise.
    """
    # Verify the password
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
