from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
Base = declarative_base()
    
class User(Base):
    __tablename__ = "Users"  # Corrected _tablename_ to __tablename__
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)  # Changed Integer to String

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Fixed the function call

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)  # Added password argument
    
# Data privacy

class Data_Privacy(Base):
    __tablename__ = "Data Privacy"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    data_type = Column("Personal info", String, Integer)
    access_level = Column("Confidential", String)

def __init__(self, employee_id, data_type=None, access_level=None):
    self.employee_id = employee_id
    self.data_type = data_type
    self.access_level = access_level

def __repr__(self):
    return f"Data_Privacy(employee_id={self.employee_id}, data_type='{self.data_type}', access_level='{self.access_level}')"

# Data backup and recovery

class Data_Backup(Base):
    __tablename__ = "Data Backup"
    id = Column(Integer, primary_key=True)
    employee_id = Column("16044", Integer)
    backup_date = Column("2024/06/01", String)
    backup_location = Column("Cloud Storage", String)

def __init__(self, employee_id, backup_date=None, backup_location=None):
    self.employee_id = employee_id
    self.backup_date = backup_date
    self.backup_location = backup_location  

def __repr__(self):
    return f"Data_Backup(employee_id={self.employee_id}, backup_date='{self.backup_date}', backup_location='{self.backup_location}')"

# Data deletion

class Data_Deletion(Base):
    __tablename__ = "Data Deletion"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    deletion_date = Column("2024/06/30", String)
    deletion_method = Column("Permanent", String)

def __init__(self, employee_id, deletion_date=None, deletion_method=None):
    self.employee_id = employee_id
    self.deletion_date = deletion_date
    self.deletion_method = deletion_method 
 
def __repr__(self):
    return f"Data_Deletion(employee_id={self.employee_id}, deletion_date='{self.deletion_date}', deletion_method='{self.deletion_method}')"    

# Example of creating a session (you'll need to adjust the database URL)
engine = create_engine('sqlite:///users.db')  # Example SQLite database
Base.metadata.create_all(engine)  # Create tables
Session = sessionmaker(bind=engine)
session = Session()

# Example of adding a user
new_user = User(username='example_user')
new_user.set_password('secure4400//##')  # Set the password
session.add(new_user)
session.commit()

# Example of verifying a password

user = session.query(User).filter_by(username='example_user').first()
if user and user.verify_password('secure4400//##'):
    print("Password is valid!")
else:
    print("Invalid password.")
   

# Close the session
session.close()