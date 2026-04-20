from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    api_key = Column(String)

class APIModel(Base):
    __tablename__ = "apis"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Float)
    latency = Column(Float)
    accuracy = Column(Float)
    success_rate = Column(Float)
