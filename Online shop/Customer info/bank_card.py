"""
Secure helpers for password hashing and encrypting sensitive bank info.

Usage:
- Provide a Fernet key via environment variable FERNET_KEY (recommended) or
  create a Fernet instance and pass it into the classes/functions that need it.

Do NOT hardcode keys in source code.
"""

from dataclasses import dataclass
import os
from typing import Optional, Dict, Callable
from cryptography.fernet import Fernet, InvalidToken
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CryptoError(Exception):
    """Raised for cryptographic-related errors (invalid key, invalid token, etc.)."""


def load_fernet_from_env(env_key: str = "FERNET_KEY") -> Fernet:
    """
    Load a Fernet key from an environment variable.
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


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (passlib)."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(password, hashed)


def _mask_value(value: Optional[str], keep: int = 4) -> str:
    if not value:
        return "N/A"
    if len(value) <= keep:
        return "*" * len(value)
    return "*" * (len(value) - keep) + value[-keep:]


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


@dataclass
class BankInfo:
    account_number: Optional[str]
    routing_number: Optional[str]

    def mask_account_number(self) -> str:
        return _mask_value(self.account_number, keep=4)

    def mask_routing_number(self) -> str:
        return _mask_value(self.routing_number, keep=4)

    def validate_account_info(self) -> bool:
        """
        Validate account and routing numbers.
        - routing_number: must be 9 digits (common for US routing numbers)
        - account_number: allow typical lengths (9-17 digits) — adjust to your business rules
        """
        if not self.account_number or not self.routing_number:
            return False
        if not (9 <= len(self.account_number) <= 17) or not self.account_number.isdigit():
            return False
        if len(self.routing_number) != 9 or not self.routing_number.isdigit():
            return False
        return True

    def encrypt_account_info(self, fernet: Fernet) -> Dict[str, str]:
        """
        Encrypt stored account info using the provided Fernet instance.
        Returns dict with base64-encoded ciphertexts.
        Raises ValueError if account info invalid.
        """
        if not self.validate_account_info():
            raise ValueError("Invalid account or routing number")
        try:
            enc_acc = fernet.encrypt(self.account_number.encode()).decode()
            enc_rt = fernet.encrypt(self.routing_number.encode()).decode()
            return {"account_number": enc_acc, "routing_number": enc_rt}
        except Exception as exc:
            raise CryptoError("Encryption failed") from exc

    @staticmethod
    def decrypt_account_info(encrypted_data: Dict[str, str], fernet: Fernet) -> Dict[str, str]:
        """
        Decrypt a dict produced by encrypt_account_info and return plaintext values.
        Raises CryptoError on failure.
        """
        try:
            acc = fernet.decrypt(encrypted_data["account_number"].encode()).decode()
            rt = fernet.decrypt(encrypted_data["routing_number"].encode()).decode()
            return {"account_number": acc, "routing_number": rt}
        except (InvalidToken, KeyError) as exc:
            raise CryptoError("Decryption failed or invalid data") from exc


class BankCard:
    """
    BankCard stores encrypted PAN, expiration date, and CVV.
    By default only masked PAN is exposed. Plaintext access must be explicit.
    """

    def __init__(self, card_number: str, expiration_date: str, cvv: str, fernet: Fernet):
        """
        Provide plaintext values and a Fernet instance. The values are encrypted immediately.
        """
        if not card_number or not card_number.isdigit():
            raise ValueError("card_number must be digits-only string")
        # Optional: enforce Luhn for PANs
        if not _luhn_check(card_number):
            # Some test or token PANs won't pass; you can choose to relax this rule for test fixtures.
            raise ValueError("card_number failed Luhn check")
        self._fernet = fernet
        try:
            self.card_number_enc = fernet.encrypt(card_number.encode()).decode()
            self.expiration_date_enc = fernet.encrypt(expiration_date.encode()).decode()
            self.cvv_enc = fernet.encrypt(cvv.encode()).decode()
        except Exception as exc:
            raise CryptoError("Encryption failed") from exc

    def get_masked_pan(self) -> str:
        """Return masked PAN (e.g., ************1234). No plaintext returned."""
        try:
            pan = self._fernet.decrypt(self.card_number_enc.encode()).decode()
        except InvalidToken:
            return "****"
        return _mask_value(pan, keep=4)

    def verify_card_last4(self, last4: str) -> bool:
        """Check that the last4 digits match the PAN's last 4 digits (without exposing PAN)."""
        if not last4 or not last4.isdigit() or len(last4) != 4:
            return False
        try:
            pan = self._fernet.decrypt(self.card_number_enc.encode()).decode()
            return pan[-4:] == last4
        except InvalidToken:
            return False

    def decrypt_pan(self, auditor: Optional[Callable[[str], None]] = None) -> str:
        """
        Return plaintext PAN. This is sensitive — call only in trusted, authorized contexts.
        Optional `auditor` callable receives a short audit message (e.g., "reveal_pan:user=svcX").
        """
        try:
            pan = self._fernet.decrypt(self.card_number_enc.encode()).decode()
            if auditor:
                try:
                    auditor("pan_revealed")
                except Exception:
                    # Do not fail decryption if auditing logging fails
                    pass
            return pan
        except InvalidToken as exc:
            raise CryptoError("Decryption failed") from exc

    def decrypt_cvv(self, auditor: Optional[Callable[[str], None]] = None) -> str:
        try:
            c = self._fernet.decrypt(self.cvv_enc.encode()).decode()
            if auditor:
                try:
                    auditor("cvv_revealed")
                except Exception:
                    pass
            return c
        except InvalidToken as exc:
            raise CryptoError("Decryption failed") from exc