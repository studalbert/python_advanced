import datetime
from datetime import timedelta

import pytest
from flask import template_rendered
from module_29_testing.hw.main.app import create_app, db as _db
from module_29_testing.hw.main.models import Parking, ClientParking, Client


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://test_db.db"

    with _app.app_context():
        _db.create_all()
        client = Client(
            id=1,
            name="name",
            surname="surname",
            credit_card="4444555566667777",
            car_number="123",
        )
        parking = Parking(
            address="example address",
            opened=True,
            count_places=50,
            count_available_places=30,
        )
        client_parking = ClientParking(
            client_id=1,
            parking_id=1,
            time_in=datetime.datetime.now() - timedelta(minutes=30),
            time_out=datetime.datetime.now(),
        )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
