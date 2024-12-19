from flask import Flask
from module_15_networking_basics.homework.models import (
    get_rooms,
    init_db,
    add_rooms,
    booking_rooms,
    rooms_records,
)

app = Flask(__name__)


@app.route("/room", methods=["GET"])
def check():
    return get_rooms()


@app.route("/add-room", methods=["POST"])
def add_room():
    return add_rooms()


@app.route("/booking", methods=["POST"])
def booking_room():
    return booking_rooms()


if __name__ == "__main__":
    init_db(initial_records=rooms_records)
    app.run(debug=True)
