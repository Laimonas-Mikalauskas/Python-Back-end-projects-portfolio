import os
import re
from typing import Optional

from cryptography.fernet import Fernet
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

DB_PATH = "customers.db"
KEY_PATH = ".fernet_key"


def get_or_create_encryption_key() -> bytes:
    """
    Use an environment variable if available; otherwise store a key on disk.
    This keeps the key stable across script runs.
    """
    env_key = os.getenv("CUSTOMER_ENCRYPTION_KEY")
    if env_key:
        return env_key.encode()

    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            return f.read().strip()

    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key


encryption_key = get_or_create_encryption_key()
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Session = sessionmaker(bind=engine)


def encrypt_data(data: Optional[str], key: bytes) -> Optional[str]:
    if data is None:
        return None
    return Fernet(key).encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: Optional[str], key: bytes) -> Optional[str]:
    if encrypted_data is None:
        return None
    return Fernet(key).decrypt(encrypted_data.encode()).decode()


# -------------------------
# Models
# -------------------------

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(32), nullable=True)
    address = Column(String(255), nullable=True)

def __init__(self, inValue):
    """
    Purpose: value
    """
    
    self.value = inValue
   # end alternate constructor 

    def __init__(
        self,
        name: str,
        email: str,
        phone_number: Optional[str] = None,
        address: Optional[str] = None,
    ):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}')>"


class FacebookInfo(Base):
    __tablename__ = "facebook_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    facebook_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    username = Column(String(100), nullable=True)

    customer = relationship("Customer", back_populates="facebook_info")

    def __init__(self, facebook_id: str, user_id: int, username: Optional[str] = None):
        self.facebook_id = facebook_id
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return (
            f"<FacebookInfo(id={self.id}, facebook_id='{self.facebook_id}', "
            f"customer_id={self.user_id})>"
        )


class DebitCard(Base):
    __tablename__ = "debit_cards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_number = Column(String(255), nullable=False)
    expiration_date = Column(String(255), nullable=False)
    cvv = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="debit_cards")

    def __init__(
        self,
        customer_id: int,
        card_number: str,
        expiration_date: str,
        cvv: str,
    ):
        self.customer_id = customer_id
        self.card_number = encrypt_data(card_number, encryption_key)
        self.expiration_date = encrypt_data(expiration_date, encryption_key)
        self.cvv = encrypt_data(cvv, encryption_key)

    def __repr__(self):
        return f"<DebitCard(id={self.id}, customer_id={self.customer_id})>"


# -------------------------
# Validation helpers
# -------------------------

def validate_email(email: str) -> bool:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, email))


def validate_card_number(card_number: str) -> bool:
    digits_only = re.sub(r"\D", "", card_number)
    return len(digits_only) in (13, 15, 16)


# -------------------------
# Customer CRUD
# -------------------------

def create_customer(
    session,
    name: str,
    email: str,
    phone_number: Optional[str] = None,
    address: Optional[str] = None,
):
    if not name or not email:
        raise ValueError("Name and email are required.")
    if not validate_email(email):
        raise ValueError("Invalid email format.")
    if session.query(Customer).filter(Customer.email == email).first():
        raise ValueError(f"Customer with email '{email}' already exists.")

    customer = Customer(
        name=name,
        email=email,
        phone_number=phone_number,
        address=address,
    )
    session.add(customer)
    session.commit()
    return customer


def get_customer_by_id(session, customer_id: int):
    return session.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(session, email: str):
    return session.query(Customer).filter(Customer.email == email).first()


def verify_customer(session, email: str) -> bool:
    return get_customer_by_email(session, email) is not None


def update_customer(
    session,
    customer_id: int,
    name=None,
    email=None,
    phone_number=None,
    address=None,
):
    customer = get_customer_by_id(session, customer_id)
    if not customer:
        return None

    if name is not None:
        customer.name = name
    if email is not None:
        if not validate_email(email):
            raise ValueError("Invalid email format.")
        customer.email = email
    if phone_number is not None:
        customer.phone_number = phone_number
    if address is not None:
        customer.address = address

    session.commit()
    return customer


def delete_customer(session, customer_id: int) -> bool:
    customer = get_customer_by_id(session, customer_id)
    if not customer:
        return False
    session.delete(customer)
    session.commit()
    return True


# -------------------------
# Facebook info CRUD
# -------------------------

def create_facebook_info(session, customer_id: int, facebook_id: str, username: Optional[str] = None):
    customer = get_customer_by_id(session, customer_id)
    if not customer:
        raise ValueError(f"No customer found with ID {customer_id}.")

    existing = session.query(FacebookInfo).filter(FacebookInfo.facebook_id == facebook_id).first()
    if existing:
        raise ValueError(f"Facebook info for ID '{facebook_id}' already exists.")

    info = FacebookInfo(
        facebook_id=facebook_id,
        user_id=customer_id,
        username=username,
    )
    session.add(info)
    session.commit()
    return info

def encrypt_facebook_info(session, facebook_info: str):
    return encrypt_data(facebook_info, encryption_key)

# -------------------------
# Debit card helpers
# -------------------------

def create_debit_card(session, customer_id: int, card_number: str, expiration_date: str, cvv: str):
    customer = get_customer_by_id(session, customer_id)
    if not customer:
        raise ValueError(f"No customer found with ID {customer_id}.")

    if not validate_card_number(card_number):
        raise ValueError("Invalid card number.")

    card = DebitCard(
        customer_id=customer_id,
        card_number=card_number,
        expiration_date=expiration_date,
        cvv=cvv,
    )
    session.add(card)
    session.commit()
    return card


def encrypt_debit_card(card: DebitCard):
    return {
        "card_number": encrypt_data(card.card_number, encryption_key),
        "expiration_date": encrypt_data(card.expiration_date, encryption_key),
        "cvv": encrypt_data(card.cvv, encryption_key),
    }


def decrypt_debit_card(card: DebitCard):
    return {
        "card_number": decrypt_data(card.card_number, encryption_key),
        "expiration_date": decrypt_data(card.expiration_date, encryption_key),
        "cvv": decrypt_data(card.cvv, encryption_key),
    }


def delete_debit_card(session, card_id: int) -> bool:
    card = session.query(DebitCard).filter(DebitCard.id == card_id).first()
    if not card:
        return False
    session.delete(card)
    session.commit()
    return True


def update_debit_card(session, card_id: int, card_number=None, expiration_date=None, cvv=None):
    card = session.query(DebitCard).filter(DebitCard.id == card_id).first()
    if not card:
        return None

    if card_number is not None:
        if not validate_card_number(card_number):
            raise ValueError("Invalid card number.")
        card.card_number = encrypt_data(card_number, encryption_key)

    if expiration_date is not None:
        card.expiration_date = encrypt_data(expiration_date, encryption_key)

    if cvv is not None:
        card.cvv = encrypt_data(cvv, encryption_key)

    session.commit()
    return card


# -------------------------
# Display helpers
# -------------------------

def print_customer_info(customer: Customer):
    print(f"Customer ID: {customer.id}")
    print(f"Name: {customer.name}")
    print(f"Email: {customer.email}")
    print(f"Phone Number: {customer.phone_number}")
    print(f"Address: {customer.address}")
    print(f"Facebook: {customer.facebook}")


def print_debit_card_info(card: DebitCard):
    decrypted = decrypt_debit_card(card)
    print(f"Debit Card ID: {card.id}")
    print(f"Card Number: {decrypted['card_number']}")
    print(f"Expiration Date: {decrypted['expiration_date']}")
    print(f"CVV: {decrypted['cvv']}")
    print(f"Customer ID: {card.customer_id}")


# -------------------------
# Database setup
# -------------------------

def create_tables():
    Base.metadata.create_all(engine)


# -------------------------
# Main menu
# -------------------------

def main_menu():
    session = Session()

    while True:
        print("\nCustomer Management Menu:")
        print("1. Create Customer")
        print("2. Retrieve Customer by ID")
        print("3. Verify Customer by Email")
        print("4. Update Customer Information")
        print("5. Delete Customer")
        print("6. Add Debit Card")
        print("7. Update Debit Card")
        print("8. View Customer's Debit Cards")
        print("9. Delete Debit Card")
        print("10. Exit")

        choice = input("Enter your choice (1-10): ")

        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")
            try:
                customer = create_customer(session, name, email, phone, address)
                print_customer_info(customer)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            customer_id = int(input("Enter customer ID: "))
            customer = get_customer_by_id(session, customer_id)
            if customer:
                print_customer_info(customer)
            else:
                print(f"No customer found with ID {customer_id}")

        elif choice == "3":
            email = input("Enter email to verify: ")
            exists = verify_customer(session, email)
            print(f"Customer exists: {exists}")

        elif choice == "4":
            customer_id = int(input("Enter customer ID to update: "))
            name = input("Enter new name (leave blank to keep current): ") or None
            email = input("Enter new email (leave blank to keep current): ") or None
            phone = input("Enter new phone number (leave blank to keep current): ") or None
            address = input("Enter new address (leave blank to keep current): ") or None

            try:
                updated_customer = update_customer(session, customer_id, name, email, phone, address)
                if updated_customer:
                    print_customer_info(updated_customer)
                else:
                    print(f"No customer found with ID {customer_id}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            customer_id = int(input("Enter customer ID to delete: "))
            deleted = delete_customer(session, customer_id)
            print(f"Customer deleted: {deleted}")

        elif choice == "6":
            customer_id = int(input("Enter customer ID: "))
            card_number = input("Enter card number: ")
            expiration = input("Enter expiration date (MM/YY): ")
            cvv = input("Enter CVV: ")
            try:
                card = create_debit_card(session, customer_id, card_number, expiration, cvv)
                print_debit_card_info(card)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "7":
            card_id = int(input("Enter card ID to update: "))
            card_number = input("Enter new card number (leave blank to keep current): ") or None
            expiration_date = input("Enter new expiration date (MM/YY) (leave blank to keep current): ") or None
            cvv = input("Enter new CVV (leave blank to keep current): ") or None

            try:
                updated_card = update_debit_card(session, card_id, card_number, expiration_date, cvv)
                if updated_card:
                    print_debit_card_info(updated_card)
                else:
                    print(f"No debit card found with ID {card_id}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "8":
            customer_id = int(input("Enter customer ID: "))
            customer = get_customer_by_id(session, customer_id)
            if not customer:
                print("Customer not found.")
                continue
            for card in customer.debit_cards:
                print_debit_card_info(card)

        elif choice == "9":
            card_id = int(input("Enter card ID to delete: "))
            deleted = delete_debit_card(session, card_id)
            print(f"Debit card deleted: {deleted}")

        elif choice == "10":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    create_tables()
    main_menu()