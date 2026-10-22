import base64
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class ShippingAddress:
    street: str
    city: str
    state: str
    zip_code: str
    country: str

    def __post_init__(self):
        self.street = (self.street or "").strip()
        self.city = (self.city or "").strip()
        self.state = (self.state or "").strip()
        self.zip_code = (self.zip_code or "").strip()
        self.country = (self.country or "").strip()

    def to_dict(self) -> dict:
        return {
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
        }

    def __str__(self):
        parts = [self.street, self.city, self.state, self.zip_code, self.country]
        return ", ".join(part for part in parts if part)

    def __bool__(self):
        return any(
            bool(v) for v in (self.street, self.city, self.state, self.zip_code, self.country)
        )


def _make_fernet_key_from_secret(secret: str) -> bytes:
    """Create a valid Fernet key from a plain-text secret."""
    return base64.urlsafe_b64encode(hashlib.sha256(secret.encode("utf-8")).digest())


def _load_fernet_from_env(env_key: str = "FERNET_KEY") -> Fernet:
    """
    Load a Fernet key from environment variable.

    Accepts either:
    1. A real Fernet key (44-char base64 string), or
    2. A plain-text secret, which is converted into a valid Fernet key.
    """
    raw = os.getenv(env_key)
    if not raw:
        raise ValueError(f"Missing encryption key in environment variable: {env_key}")

    secret = raw.strip()

    # If the value already looks like a valid Fernet key, use it directly
    try:
        return Fernet(secret.encode("utf-8"))
    except Exception:
        # Otherwise derive a valid key from the secret
        derived_key = _make_fernet_key_from_secret(secret)
        return Fernet(derived_key)


def hash_address(address: ShippingAddress) -> str:
    """Hash a shipping address using bcrypt."""
    return pwd_context.hash(str(address))


def verify_address(address: ShippingAddress, hashed: str) -> bool:
    """Verify a shipping address against a hashed address."""
    return pwd_context.verify(str(address), hashed)


def _mask_value(value: str, keep: int = 4) -> str:
    """Mask a value while preserving its last `keep` characters."""
    if keep < 0:
        raise ValueError("keep must be non-negative")

    if value is None:
        return ""

    if len(value) <= keep:
        return value

    return "*" * (len(value) - keep) + value[-keep:]


def mask_address(address: ShippingAddress, keep: int = 4) -> str:
    """Mask a shipping address, keeping the last `keep` characters of each component."""
    return (
        f"{_mask_value(address.street, keep)}, "
        f"{_mask_value(address.city, keep)}, "
        f"{_mask_value(address.state, keep)}, "
        f"{_mask_value(address.zip_code, keep)}, "
        f"{_mask_value(address.country, keep)}"
    )


@dataclass
class AddressInfo:
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

    def as_shipping_address(self) -> ShippingAddress:
        return ShippingAddress(
            street=self.street or "",
            city=self.city or "",
            state=self.state or "",
            zip_code=self.zip_code or "",
            country=self.country or "",
        )

    def mask_address(self) -> str:
        return mask_address(self.as_shipping_address())

    def validate_address_info(self) -> bool:
        """
        Validate address information.
        - street, city, state, zip_code, country must not be empty
        - zip_code must be 5 digits
        """
        if not self.street or not self.city or not self.state or not self.zip_code or not self.country:
            return False

        if len(self.zip_code) != 5 or not self.zip_code.isdigit():
            return False

        return True

    def encrypt_address(self, fernet: Fernet) -> str:
        """Encrypt the address information using Fernet symmetric encryption."""
        payload = {
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
        }
        return fernet.encrypt(json.dumps(payload, separators=(",", ":")).encode("utf-8")).decode("utf-8")

    def decrypt_address(self, fernet: Fernet, encrypted_address: str) -> "AddressInfo":
        """Decrypt the address information using Fernet symmetric encryption."""
        try:
            decrypted = fernet.decrypt(encrypted_address.encode("utf-8"))
            payload = json.loads(decrypted.decode("utf-8"))
            return AddressInfo(
                street=payload.get("street"),
                city=payload.get("city"),
                state=payload.get("state"),
                zip_code=payload.get("zip_code"),
                country=payload.get("country"),
            )
        except (InvalidToken, ValueError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Decryption failed or invalid format") from exc


if __name__ == "__main__":
    # Recommended way: set an actual Fernet key in env
    # export FERNET_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
    #
    # You can also set a plain-text secret. The code will derive a valid key from it.

    fernet = _load_fernet_from_env()

    address = AddressInfo(
        street="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="12345",
        country="USA",
    )

    print("Is valid address:", address.validate_address_info())
    print("Masked address:", address.mask_address())

    encrypted = address.encrypt_address(fernet)
    print("Encrypted address:", encrypted)

    decrypted_address = address.decrypt_address(fernet, encrypted)
    print("Decrypted address:", decrypted_address)

    shipping = ShippingAddress(
        street="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="12345",
        country="USA",
    )

    hashed = hash_address(shipping)
    print("Hashed address:", hashed)
    print("Verified:", verify_address(shipping, hashed))
