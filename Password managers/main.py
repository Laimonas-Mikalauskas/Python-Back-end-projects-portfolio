from passlib.hash import pbkdf2_sha256

def hash_password(password: str) -> str:
    """
    Hashes a password using PBKDF2 with SHA-256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies a password against a hashed value.

    Args:
        password (str): The password to verify.
        hashed (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pbkdf2_sha256.verify(password, hashed)

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.hashed_password = hash_password(password)
    
    def verify_username(self, username: str) -> bool:
        return self.username == username
        
    def __repr__(self):
        return f"User(username='{self.username}')"
    
class Password:
    def __init__(self, password: str):
        self.hashed_password = hash_password(password)
        
    def verify(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)
    
    def __repr__(self):
        return f"Password(hashed='{self.hashed_password}')"  
    
def hash_and_verify_password(password: str) -> bool:
    """
    Hashes a password and then verifies it.

    Args:
        password (str): The password to hash and verify.

    Returns:
        bool: True if the verification is successful, False otherwise.
    """
    hashed = hash_password(password)
    return verify_password(password, hashed)

if __name__ == "__main__":
    # Example usage
    user = User(username="user123", password="securepassword")
    print("Username:", user.username)
    print("Hashed Password:", user.hashed_password)
    
    # Verify username
    is_username_correct = user.verify_username("user123")
    print("Is username correct?", is_username_correct)
    
    # Verify password
    is_password_correct = verify_password("securepassword", user.hashed_password)
    print("Is password correct?", is_password_correct)
    
    # Hash and verify password
    is_verified = hash_and_verify_password("securepassword")
    print("Is password verified after hashing?", is_verified)      



