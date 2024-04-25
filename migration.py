from models.model import Base
from models.database import engine

def create():
    Base.metadata.create_all(engine)

def drop():
    Base.metadata.drop_all(engine)