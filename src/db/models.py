from db.db import Base
from sqlalchemy import Column, Integer, String


class Admins(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    user_id = Column(Integer)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    user_id = Column(Integer)
    balance = Column(Integer, default=0)
    deals = Column(Integer, default=0)
    bonus = Column(Integer, default=0)
    trade_link = Column(String)
    steam_link = Column(String)
    steam_name = Column(String)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    group = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    link = Column(String)

class Service(Base):
    __tablename__ = "servise"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)