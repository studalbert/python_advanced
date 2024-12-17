import sqlite3
from flask import request, jsonify
from typing import Optional, List
import json


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect("hw_1.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='hotel_rooms'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `hotel_rooms` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    floor INTEGER, 
                    guestNum INTEGER,
                    beds INTEGER,
                    price INTEGER,
                    booking INTEGER 
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `hotel_rooms`
                (floor, guestNum, beds, price) VALUES (?, ?, ?, ?)
                """,
                [
                    (item["floor"], item["guestNum"], item["beds"], item["price"])
                    for item in initial_records
                ],
            )


rooms_records = [
    {"floor": 2, "guestNum": 1, "beds": 1, "price": 2000},
    {"floor": 1, "guestNum": 2, "beds": 1, "price": 2500},
]


def get_rooms():
    rooms = []
    with sqlite3.connect("hw_1.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select * from hotel_rooms where booking is null;",
        )
        res = cursor.fetchall()
        for room in res:
            res_dict = {
                "roomId": room[0],
                "floor": room[1],
                "guestNum": room[2],
                "beds": room[3],
                "price": room[4],
            }
            rooms.append(res_dict)
    result_dict = {"rooms": rooms}
    return jsonify(result_dict)


def add_rooms():
    form_data = request.get_data(as_text=True)
    data_object = json.loads(form_data)
    rooms = []
    with sqlite3.connect("hw_1.db") as conn:
        cursor = conn.cursor()
        sql_query = "insert into hotel_rooms (floor, guestNum, beds, price) values (?, ?, ?, ?);"
        params = (
            data_object["floor"],
            data_object["guestNum"],
            data_object["beds"],
            data_object["price"],
        )
        cursor.execute(sql_query, params)
        cursor.execute("select * from hotel_rooms where booking is null")
        res = cursor.fetchall()
        for room in res:
            res_dict = {
                "roomId": room[0],
                "floor": room[1],
                "guestNum": room[2],
                "beds": room[3],
                "price": room[4],
            }
            rooms.append(res_dict)
    result_dict = {"rooms": rooms}
    return jsonify(result_dict)


def booking_rooms():
    form_data = request.get_data(as_text=True)
    data_object = json.loads(form_data)
    with sqlite3.connect("hw_1.db") as conn:
        cursor = conn.cursor()
        sql_query = "select * from hotel_rooms where id = ?;"
        roomId = data_object["roomId"]
        cursor.execute(sql_query, (roomId,))
        res = cursor.fetchone()
        if not res[5]:
            cursor.execute("update hotel_rooms set booking=1 where id=?;", (roomId,))
            return "ok", 200
        else:
            return "Эта комната уже забронирована", 409
