import json
import datetime

import pytest
from module_29_testing.hw.main.models import Parking, ClientParking, Client


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(client):
    client_data = {
        "name": "Иван",
        "surname": "Иванов",
        "credit_card": "1111222233334444",
        "car_number": "456",
    }
    resp = client.post("/clients", json=client_data)
    assert resp.status_code == 201
    assert resp.json["id"] == 2


def test_create_parking(client):
    parking_data = {
        "address": "example address",
        "opened": True,
        "count_places": 70,
        "count_available_places": 30,
    }
    resp = client.post("/parkings", json=parking_data)
    assert resp.status_code == 201
    assert resp.json["id"] == 2


@pytest.mark.parking
def test_create_client_parking(db, client):
    client_parking_data = {
        "client_id": 1,
        "parking_id": 1,
    }
    resp = client.post("/client_parkings", json=client_parking_data)
    assert resp.status_code == 201
    assert resp.json["id"] == 2
    parking = db.session.query(Parking).get(client_parking_data["parking_id"])

    # количество свободных мест на парковке уменьшается
    assert parking.count_available_places == 29

    # тест при закрытой парковки
    parking = Parking(
        address="example address",
        opened=False,
        count_places=50,
        count_available_places=30,
    )
    db.session.add(parking)
    db.session.commit()
    client_parking_data["parking_id"] = 2
    resp = client.post("/client_parkings", json=client_parking_data)
    assert resp.status_code == 400
    assert resp.json == {"message": "Sorry, the parking is closed."}


@pytest.mark.parking
def test_delete_client_parking(db, client):
    client_parking = ClientParking(
        client_id=1,
        parking_id=1,
        time_in=datetime.datetime.now() - datetime.timedelta(minutes=30),
    )
    db.session.add(client_parking)
    db.session.commit()
    client_parking_data = {
        "client_id": 1,
        "parking_id": 1,
    }
    resp = client.delete("/client_parkings", json=client_parking_data)
    assert resp.status_code == 200
    parking = db.session.query(Parking).get(client_parking_data["parking_id"])
    client_parking = db.session.query(ClientParking).get(2)

    # количество свободных мест на парковке увеличивается
    assert parking.count_available_places == 31

    # появляется время выезда
    assert client_parking.time_out is not None
    assert client_parking.time_out > client_parking.time_in

    # при оплате — у клиента не привязана карта
    client_example = Client(
        id=2,
        name="name",
        surname="surname",
        car_number="123",
    )
    db.session.add(client_example)
    db.session.commit()
    client_parking = ClientParking(
        client_id=2,
        parking_id=1,
        time_in=datetime.datetime.now() - datetime.timedelta(minutes=30),
    )
    db.session.add(client_parking)
    db.session.commit()
    client_parking_data = {
        "client_id": 2,
        "parking_id": 1,
    }
    resp = client.delete("/client_parkings", json=client_parking_data)
    assert resp.status_code == 400
    assert resp.json == {"error": "The client doesn't have a bank card linked"}
