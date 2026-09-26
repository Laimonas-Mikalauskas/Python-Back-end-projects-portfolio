import sys

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, UniqueConstraint  # type: ignore[import]
from sqlalchemy.orm import sessionmaker, declarative_base  # type: ignore[import]

Base = declarative_base()                                                                                                                                                                                                                                                   
engine = create_engine('sqlite:///developers.db', echo=False)
Session = sessionmaker(bind=engine)


# Table name is defined by the Employee.__tablename__ attribute

class Employee(Base):
    __tablename__ = "Employees"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    birthday = Column(Integer)
    role = Column(String)
    started_working = Column(Integer)
    salary = Column(Integer)
    experience = Column(Integer)
    tools = Column(String)
   
    def __init__(self, name, surname, birthday, role, started_working, salary, experience, tools):
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.role = role
        self.started_working = started_working
        self.salary = salary
        self.experience = experience
        self.tools = tools
                         
def __repr__(self):
    return f"Employee(id={self.id}, name='{self.name}', surname='{self.surname}', birthday={self.birthday}, role='{self.role}', started_working={self.started_working}, salary={self.salary}, experience={self.experience}, tools='{self.tools}')"

class Chief_Executive_Officer(Base):
    __tablename__ = "CEO"
    id = Column(Integer, primary_key=True)
    name = Column("Chris", String)
    surname = Column("Parker", String)
    birthday = Column("1970", Integer)
    role = Column("Chief Executive Officer", String)
    started_working = Column("2010/01/01", Integer)
    salary = Column("8000", Integer)
    experience = Column("15 years", Integer)

def __init__(self):
    self.name = "Chris"
    self.surname = "Parker"
    self.birthday = "1970"
    self.role = "Chief Executive Officer"
    self.started_working = "2010/01/01"
    self.salary = "8000"
    self.experience = "15 years"

def __repr__(self):
    return f"Chief_Executive_Officer(id={self.id}, name='{self.name}', surname='{self.surname}', birthday={self.birthday}, role='{self.role}', started_working={self.started_working}, salary={self.salary}, experience={self.experience}')"

name = "Chris"
print("Chris")
print(type("Chris"))

surname = "Parker"
print("Parker")
print(type("Parker"))

birthday = "1970"
print("1970")
print(type("1970"))

role = "Chief Executive Officer"
print("Chief Executive Officer")
print(type("Chief Executive Officer"))

started_working = "2010/01/01"
print("2010/01/01")
print(type("2010/01/01"))

salary = "8000"
print("8000")
print(type("8000"))

experience = "15 years"
print("15 years")
print(type("15 years"))


class Personal_Managers(Base):
    __tablename__ = "Personal Managers"
    id = Column(Integer, primary_key=True)
    name = Column("Alice, Charlie", String)
    surname = Column("Smith, Watson", String)
    position = Column("Personal Manager", String)
    started_working = Column("2010", String)
    salary = Column("4000", Integer)
    experience = Column("4 years", String)

def __init__(self, name: str, surname: str):
    self.name = name
    self.surname = surname
    self.position = "Personal Manager"
    self.started_working = "2010"
    self.salary = "4000"
    self.experience = "4 years"

def __repr__(self):
    return f"Personal_Managers(id={self.id}, name='{self.name}', surname='{self.surname}', position='{self.position}', started_working='{self.started_working}', salary={self.salary}, experience='{self.experience}')"

name = "Alice"
print("Alice")
print(type("Alice"))

surname = "Smith"
print("Smith")
print(type("Smith"))

name = "Charlie"
print("Charlie")
print(type("Charlie"))

surname="Watson"
print("Watsom")
print(type("Watson"))

position = "Personal Manager"
print("Personal Manager")
print(type("Personal Manager"))

started_working = "2010"
print("2010")
print(type("2010"))

salary = "4000"
print("4000")
print(type("4000"))

experience = "4 years"
print("4 years")
print(type("4 years"))

    
class Python_Developer(Base):
    __tablename__ = "Python"
    id = Column(Integer, primary_key=True)
    name = Column("Garry", String)
    surname = Column("Peterson", String)
    birthday = Column("1990", Integer)
    role = Column("Python Developer", String)
    started_working = Column("2015/06/30", Integer)
    salary = Column("5000", Integer)
    experience = Column("7 years", Integer)

    def __init__(self):
        self.name = "Garry"
        self.surname ="Peterson"
        self.birthday = "1990"
        self.role = "Python Developer"
        self.started_working = "2015/06/30"
        self.salary = "5000"
        self.experience = "7 years"

    def __repr__(self):
        return f"{self.name} {self.surname} {self.birthday} {self.role} {self.tools} {self.started_working} {self.salary} {self.experience}"

name = "Garry"
print("Garry")
print(type("Garry"))

surname = "Peterson"
print("Peterson")
print(type("Peterson"))

birthday = "1990"
print("1990")
print(type("1990"))

role = "Python Developer"
print("Python Developer")
print(type("Python Developer"))

started_working = "2015/06/30"
print("2015/06/30")
print(type("2015/06/30"))

salary = "5000"
print("5000")
print(type("5000"))

experience = "10 years"
print("10 years")
print(type("10 years"))

class Software_Developer(Base):
    __tablename__ = "Software"
    id = Column(Integer, primary_key=True)
    name = Column("Josh", String)
    surname = Column("Keller", String)
    birthday = Column("1996", Integer)
    role = Column("Software Developer", String)
    started_working = Column("2019/09/25", Integer)
    salary = Column("4000", Integer)
    experience = Column("6 years", Integer)

def __init__(self):
    self.name = "Josh"
    self.surname = "Keller"
    self.birthday = "1996"
    self.role = "Software Developer"
    self.started_working = "2019/09/25"
    self.salary = "4000"
    self.experience = "6 years"

def __repr__(self):
    return f"{self.name} {self.surname} {self.birthday} {self.role} {self.tools} {self.started_working} {self.salary} {self.experience}"

name = "Josh"
print("Josh")
print(type("Josh"))

surname = "Keller"
print("Keller")
print(type("Keller"))

birthday = "1996"
print("1996")
print(type("1996"))

role = "Software Developer"
print("Software Developer")
print(type("Software Engineer")) 
      
started_working = "2019/09/25"
print("2019/09/25")
print(type("2019/09/25"))

salary = "4000"
print("4000")
print(type("4000"))

experience = "6 years"
print("6 years")
print(type("6 years"))

class Data_Analyst(Base):
    __tablename__ = "Data"
    id = Column(Integer, primary_key=True)
    name = Column("Jack", String)
    surname = Column("Mills", String)
    birthday = Column("1990", Integer)
    role = Column("Data Analyst", String)
    started_working = Column("2021/09/25", Integer)
    salary = Column("3000", Integer)
    experience = Column("4 years", Integer)

def __init__(self):
    self.name = "Jack"
    self.surname = "Mills"
    self.birthday = "1990"
    self.role = "Data Analyst"
    self.started_working = "2021/09/25"
    self.salary = "3000"
    self.experience = "4 years"

def __str__(self):
    return f"{self.name} {self.surname} {self.birthday} {self.role} {self.started_working} {self.salary} {self.experience}"

name = "Jack"
print("Jack")
print(type("Jack"))

surname = "Mills"
print("Mills")
print(type("Mills"))

birthday ="1990"
print("1990")
print(type("1990"))

role = "Data Analyst"
print("Data Analyst")
print(type("Data Analyst"))


started_working = "2021/09/25"
print("2021/09/25")
print(type("2021/09/25"))

salary = "3000"
print("3000")
print(type("3000"))

experience = "4 years"
print("4 years")
print(type("4 years"))

class Database_Administrator(Base):
    __tablename__ = "SQL Database Administrator"
    id = Column(Integer, primary_key=True)
    name = Column("Mark", String)
    surname = Column("Wheeler", String)
    birthday = Column("1993", Integer)
    role = Column("Database Administrator", String)
    started_working = Column("2023/09/25", Integer)
    salary = Column("2500", Integer)
    experience = Column("2 years", Integer)

    def __init__(self):
        self.name = "Mark"
        self.surname = "Wheeler"
        self.birthday = "1993"
        self.role = "Database Administrator"
        self.started_working = "2023/09/25"
        self.salary = "2500"
        self.experience = "2 years"

def __str__(self):
    return f"{self.name} {self.surname} {self.birthday} {self.role} {self.started_working} {self.salary} {self.experience}"

name = "Mark"
print("Mark")
print(type("Mark"))

surname = "Wheeler"
print("Wheeler")
print(type("Wheeler"))

birthday = "1993"
print("1993")
print(type("1993"))

role = "Database Administrator"
print("Database Administrator")
print(type("Database Administrator"))

started_working = "2023/09/25"
print("2023/09/25")
print(type("2023/09/25"))

salary = "2500"
print("2500")
print(type("2500"))

experience = "2 years"
print("2 years")
print(type("2 years"))

class Technical_Skills(Base):
    __tablename__ = "Skills"
    id = Column(Integer, primary_key=True)
    skill_name = Column("Visual Studio Code, Git, GitHub", String)

def __init__(self, skill_name: str):
    self.skill_name = skill_name

def __repr__(self):
    return f"Skills(id={self.id}, skill_name='{self.skill_name}')"

print("Visual Studio Code, Git, GitHub")
print(type("Visual Studio Code, Git, GitHub"))

class Certifications(Base):
    __tablename__ = "Certifications"
    id = Column(Integer, primary_key=True)
    certification_name = Column("Certified Python Developer, Certified Software Developer, Certified Data Analyst, Certified Database Administrator", String)

def __init__(self, certification_name: str):
        self.certification_name = certification_name

def __repr__(self):    
    return f"Certifications(id={self.id}, certification_name='{self.Certified_Python_Developer, self.Certified_Software_Developer, self.Certified_Data_Analyst, self.Certified_Database_Administrator}')"

print("Certified Python Developer, Certified Software Developer, Certified Data Analyst, Certified Database Administrator")
print(type("Certified Python Developer, Certified Software Developer, Certified Data Analyst, Certified Database Administrator"))

class Projects(Base):
    __tablename__ = "Projects"
    id = Column(Integer, primary_key=True)
    project_name = Column(String)

def __init__(self, project_name: str):
    self.project_name = project_name

def __repr__(self):
    return f"Projects(id={self.id}, project_name='{self.project_name}')"

print("Project 1, Project 2, Project 3")

class Languages(Base):
    __tablename__ = "Languages"
    id = Column(Integer, primary_key=True)
    language_name = Column("Python, SQL", String)

def __init__(self, language_name: str):
        self.language_name = language_name

def __repr__(self):
    return f"Languages(id={self.id}, language_name='{self.Python, self.SQL}')"

print("Python, SQL")
print(type("Python, SQL"))
  
Base.metadata.create_all(engine)


# Manage employees data

Menu = "Workplace Menu"
print("Workplace Menu")
print(type("Workplace Menu"))

def add_employee():
    name = input("Name: ").strip()
    surname = input("Surname: ").strip()
    birthday = input("Birthday: ").strip()
    role = input("Role: ").strip()
    started_working = input("started_working: ").strip()
    salary = input("Integer: ").strip()
    experience = input("experience: ").strip()
    tools = input("Tools: ").strip()
    session = Session()
    
    try:
        employee = role(name=name, surname=surname, birthday=int("1990"), role=str("Python developer"), started_working=int("2015/06/30"), salary=int("5000"), experience=int("5 years"), tools="Visual Studio Code, Git, GitHub")
        session.add(employee)
        session.commit()
        print("Employee added")
    except Exception as e:
        session.rollback()
        print("Failed to add employee:", e)
    finally:
        session.close()

def update_employee():
    session = Session()
    try:
        employee_id = int(input("Employee ID to update: "))
        employee = session.query().get(employee_id)
        if not employee:
            print("Employee is found.")
            return

        print(f"Current position: {employee.position}")
        new_position = input("New position (leave blank to keep): ").strip()
        if new_position:
            employee.position = new_position

        session.commit()
        print("Employee updated")
    except Exception as e:
        session.rollback()
        print("Update succeeded:", e)
    finally:
        session.close()


def delete_employee():
    session = Session()
    try:
        employee_id = int(input("Employee ID to delete:"))
        employee = session.query("Employee").get(employee_id)
        if not employee:
            print("Employee not found")
            return
        session.delete(employee)
        session.commit()
        print("Employee deleted")
    except Exception as e:
        session.rollback()
        print("Failed to delete:", e)
    finally:
        session.close()

def add_position(param):
    pass
def update_position(param):
    pass
def delete_position(param):
    pass
def add_salary(param):
    pass
def update_salary(param):
    pass
def delete_salary(param):
    pass
def add_experience(param):
    pass
def update_experience(param):
    pass
def delete_experience(param):
    pass
def list_employees(param):
    pass

def main():
    actions = {
        '1': add_employee,
        '2': add_position,
        '3': add_salary,
        '4': add_experience,
        '5': update_employee,
        '6': update_position,
        '7': update_salary,
        '8': update_experience,
        '9': delete_employee,
        '10': delete_position,
        '11': delete_salary,
        '12': delete_experience,
        '13': list_employees,
        '0': lambda: sys.exit("Exiting..."),
        }

    while True:
        print("Workplace Menu")
        print("1. Add Employee")
        print("2. Add Position")
        print("3. Add Salary")
        print("4. Add Experience")
        print("5. Update Employee")
        print("6. Update Position")
        print("7. Update Salary")
        print("8. Update Experience")
        print("9. Delete Employee")
        print("10. Delete Position")
        print("11. Delete Salary")
        print("12. Delete Experience")
        print("13. List All Employees")
        print("14. List All Positions")
        print("15. Employee job history")
        print("0. Exit")

        choice = input("Choose action: ").strip()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")



main() 
 






































































