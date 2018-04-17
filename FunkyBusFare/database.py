"""
schemas for database
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import create_engine, String, Integer, Float, DateTime, Column
 
@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

class VehiclePositions(Base):
    vehicle_id = Column(String)
    timestamp = Column(DateTime)
    label = Column(String)
    trip_id = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

def initialize(dbpath):
    engine = create_engine(dbpath)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()
