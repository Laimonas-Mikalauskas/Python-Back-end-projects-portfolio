import os

from cryptography.fernet import Fernet, InvalidToken
from nacl.exceptions import CryptoError
from passlib.context import CryptContext
from wtforms.validators import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Shipping_Address:
    def __init__(self, street: str, city: str, state: str, zip_code: str, country: str):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def __repr__(self):
        return f"ShippingAddress(street={self.street}, city={self.city}, state={self.state}, zip_code={self.zip_code}, country={self.country})"
    
def _load_fernet_from_env(env_key: str = "FERNET_KEY") -> Fernet:
    """ Load a Fernet key from an environment variable.
    Raises CryptoError if missing or invalid.
    """
    raw = os.getenv(env_key)
    if not raw:
        raise CryptoError(f"Missing encryption key in environment variable: {env_key}")
    try:
        # Accept bytes or string
        key = raw.encode() if isinstance(raw, str) else raw
        return Fernet(key)
    except Exception as exc:
        raise CryptoError("Invalid Fernet key") from exc   
    
def hash_address(address: Shipping_Address) -> str:
    """Hash a shipping address using bcrypt (passlib)."""
    address_str = f"{address.street}, {address.city}, {address.state}, {address.zip_code}, {address.country}"
    return pwd_context.hash(address_str)

def verify_address(address: Shipping_Address, hashed: str) -> bool:
    """Verify a shipping address against a hashed address."""
    address_str = f"{address.street}, {address.city}, {address.state}, {address.zip_code}, {address.country}"
    return pwd_context.verify(address_str, hashed)

def _mask_value(value: str, keep: int = 4) -> str:
    """Mask a value while preserving its last ``keep`` characters."""
    if keep < 0:
        raise ValueError("keep must be non-negative")
    if len(value) <= keep:
        return value
    return "*" * (len(value) - keep) + value[-keep:]

def mask_address(address: Shipping_Address, keep: int = 4) -> str:
    """Mask a shipping address, keeping the last 'keep' characters of each component."""
    masked_street = _mask_value(address.street, keep)
    masked_city = _mask_value(address.city, keep)
    masked_state = _mask_value(address.state, keep)
    masked_zip_code = _mask_value(address.zip_code, keep)
    masked_country = _mask_value(address.country, keep)
    return f"{masked_street}, {masked_city}, {masked_state}, {masked_zip_code}, {masked_country}"     
    
    
def _luhn_check(number: str) -> bool:
    """Return True if number passes Luhn algorithm; digits only expected."""
    digits = [int(d) for d in number if d.isdigit()]
    if len(digits) < 12:  # typical minimum length for PANs
        return False
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d = d * 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


class AddressInfo:
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]

    def mask_address(self) -> str:
        return mask_address(Shipping_Address(
            street=self.street or "",
            city=self.city or "",
            state=self.state or "",
            zip_code=self.zip_code or "",
            country=self.country or ""
        ))
        
    def validate_address_info(self) -> bool:
        """
        Validate address information.
        - street: must not be empty
        - city: must not be empty
        - state: must not be empty
        - zip_code: must be 5 digits (common for US ZIP codes)
        - country: must not be empty
        """
        if not self.street or not self.city or not self.state or not self.zip_code or not self.country:
            return False
        if len(self.zip_code) != 5 or not self.zip_code.isdigit():
            return False
        return True
    
    def encrypt_address(self, fernet: Fernet) -> str:
        """Encrypt the address information using Fernet symmetric encryption."""
        address_str = f"{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"
        return fernet.encrypt(address_str.encode()).decode()
    
    def decrypt_address(self, fernet: Fernet, encrypted_address: str) -> 'AddressInfo':
        """Decrypt the address information using Fernet symmetric encryption."""
        try:
            decrypted_bytes = fernet.decrypt(encrypted_address.encode())
            decrypted_str = decrypted_bytes.decode()
            street, city, state, zip_code, country = decrypted_str.split(", ")
            return AddressInfo(street=street, city=city, state=state, zip_code=zip_code, country=country)
        except (InvalidToken, ValueError) as e:
            raise ValueError("Decryption failed or invalid format") from e


if __name__ == "__main__":
    fernet = _load_fernet_from_env()
    address = AddressInfo(street="123 Main St", city="Anytown", state="CA", zip_code="12345", country="USA")

    # Validate address
    print("Is valid address:", address.validate_address_info())

    # Mask address
    print("Masked address:", address.mask_address())

    # Encrypt address
    encrypted = address.encrypt_address(fernet)
    print("Encrypted address:", encrypted)

    # Decrypt address
    decrypted_address = address.decrypt_address(fernet, encrypted)
    print("Decrypted address:", decrypted_address)        
                


    
    
    
    
