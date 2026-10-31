from sqlalchemy import create_engine,Integer,String,Float,Column,ForeignKey
from sqlalchemy.orm import declarative_base,sessionmaker,relationship

engine = create_engine("sqlite:///db/session.db",echo=True)

base = declarative_base()

class Person(base):
    __tablename__ = "person"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=True)
    age = Column(Integer)

    things = relationship("Thing",back_populates='person')

class Thing(base):
    __tablename__="thing"
    id = Column(Integer,primary_key=True)
    desc = Column(String,nullable=True)
    value = Column(Float)
    owner = Column(Integer,ForeignKey('person.id'))

    person = relationship("Person",back_populates='things')

base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

new_person = Person(name="Malek",age=22)
session.add(new_person)
session.flush()
new_thing = Thing(desc="idk tbh",value=1.2,owner=new_person.id)
session.add(new_thing)
session.commit()