from cryptography.fernet import Fernet
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.hash import pbkdf2_sha256
from tabulate import tabulate
from datetime import datetime
import time

# Initialize database
engine = create_engine('sqlite:///password_manager.db', echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Global encryption key - should be stored securely in production
FERNET_KEY = Fernet.generate_key()

# ===== DATABASE MODELS =====

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Relationships
    password_entries = relationship("PasswordEntry", back_populates="user", cascade="all, delete-orphan")
    security_questions = relationship("SecurityQuestion", back_populates="user", cascade="all, delete-orphan")
    password_history = relationship("PasswordHistory", back_populates="user", cascade="all, delete-orphan")
    session_tokens = relationship("SessionToken", back_populates="user", cascade="all, delete-orphan")
    two_factor_auth = relationship("TwoFactorAuth", back_populates="user", cascade="all, delete-orphan")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    password_strength = relationship("PasswordStrength", back_populates="user", cascade="all, delete-orphan")

    def hash_password(self, password):
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.hashed_password)

class PasswordEntry(Base):
    __tablename__ = 'password_entries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    service_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    user = relationship("User", back_populates="password_entries")

    def encrypt_password(self, password):
        fernet = Fernet(FERNET_KEY)
        return fernet.encrypt(password.encode()).decode()

    def decrypt_password(self):
        fernet = Fernet(FERNET_KEY)
        return fernet.decrypt(self.encrypted_password.encode()).decode()

class SecurityQuestion(Base):
    __tablename__ = 'security_questions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question = Column(String, nullable=False)
    answer_hash = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    user = relationship("User", back_populates="security_questions")

    def hash_answer(self, answer):
        return pbkdf2_sha256.hash(answer)

    def verify_answer(self, answer):
        return pbkdf2_sha256.verify(answer, self.answer_hash)

class PasswordHistory(Base):
    __tablename__ = 'password_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    user = relationship("User", back_populates="password_history")

    def hash_password(self, password):
        return pbkdf2_sha256.hash(password)

class PasswordPolicy(Base):
    __tablename__ = 'password_policies'
    
    id = Column(Integer, primary_key=True)
    min_length = Column(Integer, nullable=False, default=8)
    require_uppercase = Column(Boolean, nullable=False, default=True)
    require_lowercase = Column(Boolean, nullable=False, default=True)
    require_numbers = Column(Boolean, nullable=False, default=True)
    require_special_characters = Column(Boolean, nullable=False, default=True)

class SessionToken(Base):
    __tablename__ = 'session_tokens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(Integer, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    user = relationship("User", back_populates="session_tokens")

class TwoFactorAuth(Base):
    __tablename__ = 'two_factor_auth'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    secret_key = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    user = relationship("User", back_populates="two_factor_auth")

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(Integer, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    user = relationship("User", back_populates="password_reset_tokens")

class PasswordStrength(Base):
    __tablename__ = 'password_strength'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    strength_score = Column(Integer, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    user = relationship("User", back_populates="password_strength")

# Create all tables
Base.metadata.create_all(bind=engine)

# ===== TERMINAL OUTPUT FUNCTIONS =====

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title.center(66)}")
    print("=" * 70)

def print_success(message):
    """Print success message."""
    print(f"✓ {message}")

def print_error(message):
    """Print error message."""
    print(f"✗ {message}")

def print_info(message):
    """Print info message."""
    print(f"ℹ {message}")

def print_separator():
    """Print a separator line."""
    print("-" * 70)

def print_users_table(users):
    """Print users in a formatted table."""
    if not users:
        print_error("No users found.")
        return
    
    data = []
    for user in users:
        data.append([
            user.id,
            user.username,
            user.created_at,
            len(user.password_entries)
        ])
    
    headers = ["ID", "Username", "Created At", "Password Entries"]
    print("\n" + tabulate(data, headers=headers, tablefmt="grid"))

def print_password_entries_table(entries):
    """Print password entries in a formatted table."""
    if not entries:
        print_error("No password entries found.")
        return
    
    data = []
    for entry in entries:
        data.append([
            entry.id,
            entry.service_name,
            entry.username,
            entry.created_at,
            "••••••••"
        ])
    
    headers = ["ID", "Service", "Username", "Created At", "Password"]
    print("\n" + tabulate(data, headers=headers, tablefmt="grid"))

def print_security_questions_table(questions):
    """Print security questions in a formatted table."""
    if not questions:
        print_error("No security questions found.")
        return
    
    data = []
    for question in questions:
        data.append([
            question.id,
            question.question,
            question.created_at
        ])
    
    headers = ["ID", "Question", "Created At"]
    print("\n" + tabulate(data, headers=headers, tablefmt="grid"))

def print_password_history_table(history):
    """Print password history in a formatted table."""
    if not history:
        print_error("No password history found.")
        return
    
    data = []
    for entry in history:
        data.append([
            entry.id,
            entry.created_at,
            "••••••••"
        ])
    
    headers = ["ID", "Changed At", "Password Hash"]
    print("\n" + tabulate(data, headers=headers, tablefmt="grid"))

# ===== USER MANAGEMENT FUNCTIONS =====

def add_user(username, password):
    """Add a new user to the database."""
    session = SessionLocal()
    try:
        # Check if user already exists
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            print_error(f"User '{username}' already exists.")
            return None
        
        user = User(username=username, hashed_password=User(username="temp", hashed_password="temp").hash_password(password))
        session.add(user)
        session.commit()
        
        # Add to password history
        history = PasswordHistory(user_id=user.id, hashed_password=user.hash_password(password))
        session.add(history)
        session.commit()
        
        print_success(f"User '{username}' added successfully (ID: {user.id})")
        return user.id
    except Exception as e:
        session.rollback()
        print_error(f"Failed to add user: {e}")
        return None
    finally:
        session.close()

def view_all_users():
    """View all users in the system."""
    session = SessionLocal()
    try:
        users = session.query(User).all()
        print_header("ALL USERS")
        print_users_table(users)
        print_info(f"Total users: {len(users)}")
    except Exception as e:
        print_error(f"Failed to retrieve users: {e}")
    finally:
        session.close()

def view_user(user_id):
    """View a specific user's details."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        print_header(f"USER DETAILS - ID: {user_id}")
        print(f"Username:           {user.username}")
        print(f"Created:            {user.created_at}")
        print(f"Password Entries:   {len(user.password_entries)}")
        print(f"Security Questions: {len(user.security_questions)}")
    except Exception as e:
        print_error(f"Failed to retrieve user: {e}")
    finally:
        session.close()

def update_user(user_id, new_username=None, new_password=None):
    """Update user information."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        if new_username:
            # Check if new username already exists
            existing = session.query(User).filter_by(username=new_username).first()
            if existing and existing.id != user_id:
                print_error(f"Username '{new_username}' is already taken.")
                return
            user.username = new_username
        
        if new_password:
            user.hashed_password = user.hash_password(new_password)
            # Add to password history
            history = PasswordHistory(user_id=user_id, hashed_password=user.hash_password(new_password))
            session.add(history)
        
        session.commit()
        print_success("User updated successfully.")
    except Exception as e:
        session.rollback()
        print_error(f"Failed to update user: {e}")
    finally:
        session.close()

def delete_user(user_id):
    """Delete a user and all associated data."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        username = user.username
        session.delete(user)
        session.commit()
        print_success(f"User '{username}' and all associated data deleted.")
    except Exception as e:
        session.rollback()
        print_error(f"Failed to delete user: {e}")
    finally:
        session.close()

# ===== PASSWORD ENTRY FUNCTIONS =====

def add_password_entry(user_id, service_name, username, password):
    """Add a new password entry."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        entry = PasswordEntry(service_name=service_name, username=username, encrypted_password="")
        entry.user_id = user_id
        entry.encrypted_password = entry.encrypt_password(password)
        
        session.add(entry)
        session.commit()
        print_success(f"Password entry for '{service_name}' added successfully.")
    except Exception as e:
        session.rollback()
        print_error(f"Failed to add password entry: {e}")
    finally:
        session.close()

def view_password_entries(user_id):
    """View all password entries for a user."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        entries = session.query(PasswordEntry).filter_by(user_id=user_id).all()
        print_header(f"PASSWORD ENTRIES - USER: {user.username}")
        print_password_entries_table(entries)
        print_info(f"Total entries: {len(entries)}")
    except Exception as e:
        print_error(f"Failed to retrieve password entries: {e}")
    finally:
        session.close()

def view_all_password_entries():
    """View all password entries in the system."""
    session = SessionLocal()
    try:
        entries = session.query(PasswordEntry).all()
        print_header("ALL PASSWORD ENTRIES")
        print_password_entries_table(entries)
        print_info(f"Total entries: {len(entries)}")
    except Exception as e:
        print_error(f"Failed to retrieve password entries: {e}")
    finally:
        session.close()

def decrypt_password_entry(entry_id, user_id):
    """Decrypt and display a specific password entry."""
    session = SessionLocal()
    try:
        entry = session.query(PasswordEntry).filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            print_error(f"Password entry with ID {entry_id} not found.")
            return
        
        decrypted_password = entry.decrypt_password()
        print_header(f"DECRYPTED PASSWORD - ID: {entry_id}")
        print(f"Service:   {entry.service_name}")
        print(f"Username:  {entry.username}")
        print(f"Password:  {decrypted_password}")
        print(f"Created:   {entry.created_at}")
    except Exception as e:
        print_error(f"Failed to decrypt password: {e}")
    finally:
        session.close()

def update_password_entry(entry_id, user_id, new_service_name=None, new_username=None, new_password=None):
    """Update a password entry."""
    session = SessionLocal()
    try:
        entry = session.query(PasswordEntry).filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            print_error(f"Password entry with ID {entry_id} not found.")
            return
        
        if new_service_name:
            entry.service_name = new_service_name
        if new_username:
            entry.username = new_username
        if new_password:
            entry.encrypted_password = entry.encrypt_password(new_password)
        
        session.commit()
        print_success("Password entry updated successfully.")
    except Exception as e:
        session.rollback()
        print_error(f"Failed to update password entry: {e}")
    finally:
        session.close()

def delete_password_entry(entry_id, user_id):
    """Delete a password entry."""
    session = SessionLocal()
    try:
        entry = session.query(PasswordEntry).filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            print_error(f"Password entry with ID {entry_id} not found.")
            return
        
        service_name = entry.service_name
        session.delete(entry)
        session.commit()
        print_success(f"Password entry for '{service_name}' deleted.")
    except Exception as e:
        session.rollback()
        print_error(f"Failed to delete password entry: {e}")
    finally:
        session.close()

# ===== SECURITY QUESTION FUNCTIONS =====

def add_security_question(user_id, question, answer):
    """Add a security question for a user."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        sec_question = SecurityQuestion(user_id=user_id, question=question, answer_hash="")
        sec_question.answer_hash = sec_question.hash_answer(answer)
        
        session.add(sec_question)
        session.commit()
        print_success(f"Security question added successfully.")
    except Exception as e:
        session.rollback()
        print_error(f"Failed to add security question: {e}")
    finally:
        session.close()

def view_security_questions(user_id):
    """View all security questions for a user."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        questions = session.query(SecurityQuestion).filter_by(user_id=user_id).all()
        print_header(f"SECURITY QUESTIONS - USER: {user.username}")
        print_security_questions_table(questions)
        print_info(f"Total questions: {len(questions)}")
    except Exception as e:
        print_error(f"Failed to retrieve security questions: {e}")
    finally:
        session.close()

def submit_security_answer(user_id, question_id, answer):
    """Verify a security answer."""
    session = SessionLocal()
    try:
        security_question = session.query(SecurityQuestion).filter_by(id=question_id, user_id=user_id).first()
        if not security_question:
            print_error(f"Security question with ID {question_id} not found.")
            return
        
        if security_question.verify_answer(answer):
            print_success("Security answer is correct!")
        else:
            print_error("Security answer is incorrect.")
    except Exception as e:
        print_error(f"Failed to verify answer: {e}")
    finally:
        session.close()

# ===== PASSWORD HISTORY FUNCTIONS =====

def view_password_history(user_id):
    """View password change history for a user."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print_error(f"User with ID {user_id} not found.")
            return
        
        history = session.query(PasswordHistory).filter_by(user_id=user_id).all()
        print_header(f"PASSWORD HISTORY - USER: {user.username}")
        print_password_history_table(history)
        print_info(f"Total password changes: {len(history)}")
    except Exception as e:
        print_error(f"Failed to retrieve password history: {e}")
    finally:
        session.close()

# ===== MAIN MENU =====

def main():
    """Main application loop."""
    print_header("PASSWORD MANAGER")
    print_info("A secure password management system\n")
    
    while True:
        print("\n" + "-" * 70)
        print("1.  Add User")
        print("2.  View All Users")
        print("3.  View Specific User")
        print("4.  Update User")
        print("5.  Delete User")
        print("6.  Add Password Entry")
        print("7.  View All Password Entries")
        print("8.  View User Password Entries")
        print("9.  Decrypt Password Entry")
        print("10. Update Password Entry")
        print("11. Delete Password Entry")
        print("12. Add Security Question")
        print("13. View Security Questions")
        print("14. Submit Security Answer")
        print("15. View Password History")
        print("16. Exit")
        print("-" * 70)
        
        choice = input("\nSelect an option (1-16): ").strip()
        
        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if username and password:
                add_user(username, password)
            else:
                print_error("Username and password cannot be empty.")
        
        elif choice == '2':
            view_all_users()
        
        elif choice == '3':
            try:
                user_id = int(input("User ID: ").strip())
                view_user(user_id)
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '4':
            try:
                user_id = int(input("User ID: ").strip())
                new_username = input("New username (leave blank to skip): ").strip() or None
                new_password = input("New password (leave blank to skip): ").strip() or None
                if new_username or new_password:
                    update_user(user_id, new_username, new_password)
                else:
                    print_error("Please provide at least one field to update.")
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '5':
            try:
                user_id = int(input("User ID: ").strip())
                confirm = input("Are you sure you want to delete this user? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    delete_user(user_id)
                else:
                    print_info("Deletion cancelled.")
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '6':
            try:
                user_id = int(input("User ID: ").strip())
                service_name = input("Service name (e.g., Gmail): ").strip()
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                if service_name and username and password:
                    add_password_entry(user_id, service_name, username, password)
                else:
                    print_error("All fields are required.")
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '7':
            view_all_password_entries()
        
        elif choice == '8':
            try:
                user_id = int(input("User ID: ").strip())
                view_password_entries(user_id)
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '9':
            try:
                user_id = int(input("User ID: ").strip())
                entry_id = int(input("Entry ID: ").strip())
                decrypt_password_entry(entry_id, user_id)
            except ValueError:
                print_error("Invalid ID.")
        
        elif choice == '10':
            try:
                user_id = int(input("User ID: ").strip())
                entry_id = int(input("Entry ID: ").strip())
                new_service_name = input("New service name (leave blank to skip): ").strip() or None
                new_username = input("New username (leave blank to skip): ").strip() or None
                new_password = input("New password (leave blank to skip): ").strip() or None
                if new_service_name or new_username or new_password:
                    update_password_entry(entry_id, user_id, new_service_name, new_username, new_password)
                else:
                    print_error("Please provide at least one field to update.")
            except ValueError:
                print_error("Invalid ID.")
        
        elif choice == '11':
            try:
                user_id = int(input("User ID: ").strip())
                entry_id = int(input("Entry ID: ").strip())
                confirm = input("Are you sure you want to delete this entry? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    delete_password_entry(entry_id, user_id)
                else:
                    print_info("Deletion cancelled.")
            except ValueError:
                print_error("Invalid ID.")
        
        elif choice == '12':
            try:
                user_id = int(input("User ID: ").strip())
                question = input("Security question: ").strip()
                answer = input("Answer: ").strip()
                if question and answer:
                    add_security_question(user_id, question, answer)
                else:
                    print_error("Question and answer cannot be empty.")
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '13':
            try:
                user_id = int(input("User ID: ").strip())
                view_security_questions(user_id)
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '14':
            try:
                user_id = int(input("User ID: ").strip())
                question_id = int(input("Question ID: ").strip())
                answer = input("Answer: ").strip()
                submit_security_answer(user_id, question_id, answer)
            except ValueError:
                print_error("Invalid ID.")
        
        elif choice == '15':
            try:
                user_id = int(input("User ID: ").strip())
                view_password_history(user_id)
            except ValueError:
                print_error("Invalid User ID.")
        
        elif choice == '16':
            print_header("GOODBYE")
            print_info("Thank you for using Password Manager!")
            break
        
        else:
            print_error("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

