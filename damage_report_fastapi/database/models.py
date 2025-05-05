from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Avatar(Base):
    __tablename__ = 'avatar'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    file_path = Column(String(255))
    
class Weapon(Base):
    __tablename__ = 'weapon'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    file_path = Column(String(255))
    
class Artifact(Base):
    __tablename__ = 'artifact'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    file_path = Column(String(255))
    
class Character(Base):
    __tablename__ = 'character'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    element = Column(String(20))
