from flask import Flask, jsonify, request
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# type 'export FLASK_APP=application.py'
# and 'export FLASK_ENV=development'
# and type 'flask run' for running the server
Base = declarative_base()
app = Flask(__name__)


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


@app.route('/')
def index():
    return 'Hello!'


@app.route('/pets')
def get_pets():
    pets = session.query(Pet)
    output = []
    for pet in pets:
        pet_data = {'id': pet.pet_id, 'name': pet.pet_name, 'description': pet.description, 'owner': pet.owner}
        output.append(pet_data)
    return {'pets': output}


@app.route('/owners')
def get_owners():
    owners = session.query(Person)
    output = []
    for owner in owners:
        owner_data = {
            'first_name': owner.firstname,
            'last_name': owner.lastname,
            'ssn': owner.ssn,
            'age': owner.age,
            'gender': owner.gender
        }
        output.append(owner_data)
    return {'owners': output}


@app.route('/pets/<id>')
def get_pet(id):
    pet = session.query(Pet).get(id)
    return {"id": pet.pet_id, "name": pet.pet_name}


@app.route('/pets', methods=['POST'])
def add_pets():
    pet = Pet(
        pet_name=request.json['name'],
        description=request.json['description'],
        pet_id=request.json['id'],
        owner=request.json['owner']
    )
    session.add(pet)
    session.commit()
    return {'id': pet.pet_id}
