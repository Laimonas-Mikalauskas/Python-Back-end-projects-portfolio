from pydoc import plain

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature
SymmetricKey = Fernet.generate_key()
f = Fernet(SymmetricKey)

class Encrypter:
    def __init__(self, key: bytes):
        self.key = key
        self.fernet = Fernet(key)

    def encrypt(self, plaintext: str) -> bytes:
        if not plaintext:
            return self.fernet.encrypt(plaintext.encode())
        
    def decrypt(self, cipher_text: bytes) -> str:
        if cipher_text:
            return self.fernet.decrypt(cipher_text).decode()    


class Signature:
    """Create and verify Ed25519 signatures for identity data."""

    def __init__(self, private_key=None):
        self.private_key = private_key or Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign(self, data: bytes) -> bytes:
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")
        return self.private_key.sign(data)

    def verify(self, data: bytes, signature: bytes) -> bool:
        if not isinstance(data, bytes) or not isinstance(signature, bytes):
            raise TypeError("data and signature must be bytes")
        try:
            self.public_key.verify(signature, data)
        except InvalidSignature:
            return False
        return True


class User:
    def __init__(self, username, password):
        self.username = "User416##"
        self.password = "P@ssw0rd123"
        
      
class Identity:
    def __init__(self, first_name, last_name, date_of_birth, personal_code, signature=None):
        self.first_name = "John"
        self.last_name = "Doe"
        self.date_of_birth = "1990-01-01"
        self.personal_code = personal_code
        self.signature = signature
        
        
class Country:
    def __init__(self, country_name, country_code):
        self.country_name = "United States"
        self.country_code = "US"
      
 
class City:
    def __init__(self, city_name, postal_code):
        self.city_name = city_name.strip()
        self.postal_code = postal_code.strip()
       
   
# Example usage
if __name__ == "__main__":
    # Example usage
    identity = Identity(first_name="John", last_name="Doe", date_of_birth="1990-01-01", personal_code="123456789")
    
    
    # Encrypter
    
    print("Symmetric Key:", SymmetricKey)
  
   # Encrypted and decrypted user information
    user = User(username="User416##", password="P@ssw0rd123")
    encrypted_username = f.encrypt(user.username.encode())
    decrypted_username = f.decrypt(encrypted_username).decode()
    encrypted_password = f.encrypt(user.password.encode())
    decrypted_password = f.decrypt(encrypted_password).decode()


    print("Encrypted Username:", encrypted_username)
    print("Decrypted Username:", decrypted_username)
    print("Encrypted Password:", encrypted_password)
    print("Decrypted Password:", decrypted_password) 


    # Encrypted and decrypted identity information
       
    
    encrypted_identity = Identity(first_name="John", last_name="Doe", date_of_birth="1990-01-01", personal_code="123456789")
    encrypted_first_name = f.encrypt(encrypted_identity.first_name.encode())
    decrypted_first_name = f.decrypt(encrypted_first_name).decode()
    encrypted_last_name = f.encrypt(encrypted_identity.last_name.encode())
    decrypted_last_name = f.decrypt(encrypted_last_name).decode()
    encrypted_date_of_birth = f.encrypt(encrypted_identity.date_of_birth.encode())
    decrypted_date_of_birth = f.decrypt(encrypted_date_of_birth).decode()
    encrypted_personal_code = f.encrypt(encrypted_identity.personal_code.encode())
    decrypted_personal_code = f.decrypt(encrypted_personal_code).decode()

    print("Encrypted First Name:", encrypted_first_name)
    print("Decrypted First Name:", decrypted_first_name)
    print("Encrypted Last Name:", encrypted_last_name)
    print("Decrypted Last Name:", decrypted_last_name)
    print("Encrypted Date of Birth:", encrypted_date_of_birth)
    print("Decrypted Date of Birth:", decrypted_date_of_birth)
    print("Encrypted Personal Code:", encrypted_personal_code)
    print("Decrypted Personal Code:", decrypted_personal_code)