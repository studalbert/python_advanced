from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from module_29_testing.hw.main.extentions import db
from typing import Dict, Any


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))
    client_parking_assoc = db.relationship("ClientParking", back_populates="client")
    parking = association_proxy("client_parking_assoc", "parking")

    def __repr__(self):
        return f"Клиент {self.name}, {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)
    client_parking_assoc = db.relationship("ClientParking", back_populates="parking")
    parking = association_proxy("client_parking_assoc", "client")

    def __repr__(self):
        return f"Парковка {self.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, ForeignKey("parking.id"))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    # __table_args__ = (
    #     UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    # )
    client = db.relationship("Client", back_populates="client_parking_assoc")
    parking = db.relationship("Parking", back_populates="client_parking_assoc")

    def __repr__(self):
        return f"ClientParking(id={self.id}, client_id={self.client_id}, parking_id={self.parking_id})"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
