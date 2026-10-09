from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

# Create database engine and session
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id == Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    account_type = Column(String, unique=True)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', password='{self.password}'. account_type='{self.account_type}')>"

try:
    # Adding users to the database with hashed passwords
    user1 = User(name='Chris'), 
    user2 = User(name='Alice'),
    user3 = User(name='Charlie'),
    user4 = User(name="Garry"),
    user5 = User(name="Josh"),
    user6 = User(name="Jack"),
    user7 = User(name="Mark") 

    session.add(user1)
    session.add(user2)
    session.commit()

    # SQLAlchemy ORM example to prevent SQL injection
    secure_user_input = input("Enter user ID: ")

    # Validate input to ensure it's an integer
    try:
        user_id = int(secure_user_input)
        user = session.query(User).filter(User.id == user_id).first()

        if user:
            print(f"User found: {user.name}")
        else:
            print("User not found.")
    except ValueError:
        print("Please enter a valid integer for user ID.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    session.close()  # Ensure the session is closed