from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///company.db")
Session = sessionmaker(bind=engine)

Table = "Company"
print("Company")
print(type("Company"))

class Company(Base):
    __tablename__ = "Company"
    id = Column(Integer, primary_key=True)
    name = Column("Tech Innovators Inc.", String)
    location = Column("Chicago, IL", String)
    address = Column("123 Main St, Chicago, IL 60601", String)
    print("Company Name: Tech Innovators Inc.")
    print(type("Company Name: Tech Innovators Inc."))
    print("Location: Chicago, IL")
    print(type("Location: Chicago, IL"))
    print("Address: 123 Main St, Chicago, IL 60601")
    print(type("Address: 123 Main St, Chicago, IL 60601"))
    
def __init__(self, name: str, location: str):
        self.name = name
        self.location = location

def __repr__(self):
    return f"Company(id={self.id}, name='{self.name}', location='{self.location}')"

def print_company(self):
    print("Company:")
    print("1. Tech Innovators Inc.")
    print("Location: Chicago, IL")
    print("Address: 123 Main St, Chicago, IL 60601")

class Establishment(Base):
    __tablename__ = "Establishment"
    id = Column(Integer, primary_key=True)
    year_established = Column("2010", Integer)

def __init__(self, year_established: int):
        self.year_established = year_established

def __repr__(self):
    return f"Establishment(id={self.id}, year_established={self.year_established})"

def print_establishment(self):
    print("Year Established:")
    print("2010")
    print(type("2010"))

class Years_of_Service(Base):
    __tablename__ = "2012-present"
    id = Column(Integer, primary_key=True)
    years = Column("2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024", Integer)
    print("Years_of_Service 2012-present")
    print(type("Years_of_Service 2012-present"))

def print_years_of_service(self):
    print("Years of Service:")
    print(type("Years of Service"))
    print("2012")
    print(type("2012"))
    print("2013")
    print(type("2013"))
    print("2014")
    print(type("2014"))
    print("2015")
    print(type("2015"))
    print("2016")
    print(type("2016"))
    print("2017")
    print(type("2017"))
    print("2018")
    print(type("2018"))
    print("2019")
    print(type("2019"))
    print("2020")
    print(type("2020"))
    print("2021")
    print(type("2021"))
    print("2022")
    print(type("2022"))
    print("2023")
    print(type("2023"))
    print("2024")
    print(type("2024"))  
   

def __init__(self, years: int):
        self.years = years

def __repr__(self):
    return f"Years_of_Service(id={self.id}, years={self.years})"    

class Departments(Base):
    __tablename__ = "Departments"
    id = Column(Integer, primary_key=True)
    name = Column("Information Technology, Finance, Cybersecurity", String)
    print("Departments")
    print(type("Departments"))
    print("Information Technology, Finance, Cybersecurity")
    print(type("Information Technology, Finance, Cybersecurity"))

def __init__(self, name: str):
        self.name = name
        self.print_departments()

def __repr__(self):
    return f"Department(id={self.id}, name='{self.name}')"

def print_departments(self):
    print("Departments:")
    print("1. Information Technology")
    print("2. Finance")
    print("3. Cybersecurity")


class Ratings(Base):
    __tablename__ = "Ratings"
    id = Column(Integer, primary_key=True)
    rating = Column("Excellent, Good, Average, Poor", String)
    print("Ratings")
    print(type("Ratings"))
    print("Excellent, Good, Average, Poor")
    print(type("Excellent, Good, Average, Poor"))

def print_ratings(self):
    print("Ratings:")
    print("1. Excellent")
    print("2. Good")
    print("3. Average")
    print("4. Poor")        

def __init__(self, rating: str):
    self.rating = rating

def __repr__(self):
    return f"Ratings(id={self.id}, rating='{self.rating}')" 

class Awards(Base):
    __tablename__ = "Awards"
    id = Column(Integer, primary_key=True)
    award_name = Column("Employee of the Year, Innovation Award, Excellence Award, Creativity Award, Security Award", String)
    print("Awards")
    print(type("Awards"))
    print("Employee of the Year, Innovation Award, Excellence Award, Creativity Award, Security Award")
    print(type("Employee of the Year, Innovation Award, Excellence Award, Creativity Award, Security"))

def __init__(self, award_name: str):
    self.award_name = award_name

def repr(self):
    return f"Awards(id={self.id}, award_name='{self.award_name}')"

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
session.commit()
session.close()


        


