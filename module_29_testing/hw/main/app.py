import datetime

from flask import Flask, jsonify, request
from module_29_testing.hw.main.extentions import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hw3.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["DEBUG"] = True
    db.init_app(app)

    from module_29_testing.hw.main.models import Client, Parking, ClientParking

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET"])
    def get_clients():
        clients = db.session.query(Client).all()
        if clients:
            return jsonify([client.to_json() for client in clients])
        else:
            return jsonify(message="Not Found"), 404

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client(client_id):
        client = db.session.query(Client).get(client_id)
        if client:
            return jsonify(client.to_json())
        else:
            return jsonify(message="Not Found"), 404

    @app.route("/clients", methods=["POST"])
    def create_client():
        data = request.get_json()
        new_client = Client(
            name=data["name"],
            surname=data["surname"],
            credit_card=data.get("credit_card"),
            car_number=data.get("car_number"),
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.to_json()), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data = request.get_json()
        new_parking = Parking(
            address=data["address"],
            opened=data["opened"],
            count_places=data["count_places"],
            count_available_places=data["count_available_places"],
        )
        db.session.add(new_parking)
        db.session.commit()
        return jsonify(new_parking.to_json()), 201

    @app.route("/client_parkings", methods=["POST"])
    def create_client_parking():
        data = request.get_json()
        client_id = data.get("client_id")
        parking_id = data.get("parking_id")
        parking = db.session.query(Parking).get(parking_id)
        client = db.session.query(Client).get(client_id)
        if not parking or not client:
            return jsonify(message="Client or parking not found"), 404
        if not parking.opened:
            return jsonify(message="Sorry, the parking is closed."), 400
        client_parking = (
            db.session.query(ClientParking)
            .filter_by(client_id=client_id, parking_id=parking_id, time_out=None)
            .first()
        )
        if client_parking:
            return jsonify(error="A record with such data already exists"), 400
        if parking.count_available_places <= 0:
            return jsonify(error="No available parking places"), 400
        parking.count_available_places -= 1
        date = datetime.datetime.now()
        client_parking = ClientParking(
            client_id=client_id, parking_id=parking_id, time_in=date
        )
        db.session.add(client_parking)
        db.session.commit()
        return jsonify(client_parking.to_json()), 201

    @app.route("/client_parkings", methods=["DELETE"])
    def delete_client_parking():
        data = request.get_json()
        client_id = data.get("client_id")
        parking_id = data.get("parking_id")
        parking = db.session.query(Parking).get(parking_id)
        client = db.session.query(Client).get(client_id)
        if not parking or not client:
            return jsonify(message="Client or parking not found"), 404
        client_parking = (
            db.session.query(ClientParking)
            .filter_by(client_id=client_id, parking_id=parking_id, time_out=None)
            .first()
        )
        if not client_parking:
            return jsonify(error="No record with such data was found."), 400
        if not client.credit_card:
            return jsonify(error="The client doesn't have a bank card linked"), 400

        parking.count_available_places += 1
        date = datetime.datetime.now()
        client_parking.time_out = date
        db.session.commit()
        return jsonify(client_parking.to_json()), 200

    return app
