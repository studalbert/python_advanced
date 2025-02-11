from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    JSON,
    Float,
    create_engine,
    Sequence,
    Identity,
    ForeignKey,
    delete,
    ARRAY,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from flask import Flask, jsonify
from typing import Dict, Any
from sqlalchemy.dialects.postgresql import insert


engine = create_engine("postgresql+psycopg2://hw2:hw2@localhost/skillbox_db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Coffee(Base):

    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(ARRAY(String))
    users = relationship("User", back_populates="coffee")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50))
    has_sale = Column(Boolean)
    patronomic = Column(String(50))
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey("coffee.id"))
    coffee = relationship("Coffee", back_populates="users")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
