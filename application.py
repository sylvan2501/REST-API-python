from flask import Flask
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firsrname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f'({self.ssn}) ({self.firstname}) ({self.lastname}) ({self.gender}) ({self.age})'


class Pet(Base):
    __tablename__ = "pets"

    pet_id = Column("pet_id", Integer, primary_key=True)
    pet_name = Column("pet_name", String)
    description = Column("description", String)
    owner = Column(Integer, ForeignKey("people.ssn"))

    def __init__(self, pet_id, pet_name, description, owner):
        self.pet_id = pet_id
        self.pet_name = pet_name
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f'({self.pet_id}) ({self.pet_name}) ({self.description}) ({self.owner})'


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
person = Person(123456789, "Michael", "Perkins", "m", 35)
session.add(person)
session.commit()

person1 = Person(123456785, "Tim", "Lodi", "m", 23)
person2 = Person(122455789, "Dan", "Freeman", "m", 34)
person3 = Person(523458789, "Jane", "Eyre", "f", 39)
session.add(person1)
session.add(person2)
session.add(person3)
session.commit()

# results = session.query(Person).filter(Person.lastname == 'Lodi')

pet1 = Pet(8931, 'Scali', 'This is a reptilian type of creature', person1.ssn)
pet2 = Pet(4230, 'Feathery', 'This is a reptilian type of creature', person2.ssn)
pet3 = Pet(8011, 'Spiky', 'This is a reptilian type of creature', person3.ssn)
pet4 = Pet(4537, 'Slithery', 'This is a reptilian type of creature', person2.ssn)
pet5 = Pet(4411, 'Wiggly', 'This is a reptilian type of creature', person1.ssn)

session.add(pet1)
session.add(pet2)
session.add(pet3)
session.add(pet4)
session.add(pet5)
session.commit()
