import sqlite3
from flask import request, jsonify
from typing import Optional, List
import json
from datetime import datetime


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect("hw_1.db") as conn:
        # 1 table
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
                    price INTEGER
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
        # 2 table
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='room_bookings'; 
            """
        )
        res: Optional[tuple[str,]] = cursor.fetchone()
        if not res:
            cursor.executescript(
                """
                CREATE TABLE `room_bookings` (
                    room_id INTEGER, 
                    check_in_date VARCHAR(32), 
                    check_out_date VARCHAR(32),
                    first_name VARCHAR(32),
                    last_name VARCHAR(32)
                )
                """
            )


rooms_records = [
    {"floor": 2, "guestNum": 1, "beds": 1, "price": 2000},
    {"floor": 1, "guestNum": 2, "beds": 1, "price": 2500},
]


def get_rooms():
    check_in = request.args.get("checkIN")
    check_out = request.args.get("checkOut")
    guests_num = request.args.get("guestsNum", type=int)
    rooms = []
    with sqlite3.connect("hw_1.db") as conn:
        cursor = conn.cursor()
        if check_in and check_out and guests_num:
            sql_query_1 = (
                "select room_id, check_in_date, check_out_date from room_bookings"
            )
            cursor.execute(sql_query_1)
            result_room_bookings = cursor.fetchall()
            cursor.execute(
                "select * from hotel_rooms where guestNum = ?", (guests_num,)
            )
            result_hotel_rooms = cursor.fetchall()
            for room in result_hotel_rooms:
                for id, check_in_date, check_out_date in result_room_bookings:
                    start_date = datetime.strptime(check_in_date, format("%Y%m%d"))
                    end_date = datetime.strptime(check_out_date, format("%Y%m%d"))
                    if id == room[0] and (
                        start_date
                        <= datetime.strptime(check_in, format("%Y%m%d"))
                        <= end_date
                        or start_date
                        <= datetime.strptime(check_out, format("%Y%m%d"))
                        <= end_date
                    ):
                        break
                else:
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
        else:
            cursor.execute(
                "select * from hotel_rooms where id not in (select distinct(room_id) from room_bookings)"
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
        cursor.execute(
            "select * from hotel_rooms where id not in (select distinct(room_id) from room_bookings)"
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


def booking_rooms():
    form_data = request.get_data(as_text=True)
    data_object = json.loads(form_data)
    check_in = data_object["bookingDates"]["checkIn"]
    check_out = data_object["bookingDates"]["checkOut"]
    first_name = data_object["firstName"]
    last_name = data_object["lastName"]
    room_id = data_object["roomId"]
    with sqlite3.connect("hw_1.db") as conn:
        cursor = conn.cursor()
        sql_query = "select * from hotel_rooms where id = ?;"
        cursor.execute(sql_query, (room_id,))
        res = cursor.fetchone()
        if res is None:
            print("Комната с таким ID не найдена."), 400
        else:
            sql_query = "select check_in_date, check_out_date from room_bookings where room_id = ?"
            cursor.execute(sql_query, (room_id,))
            book_rooms = cursor.fetchall()
            if not book_rooms:
                sql_query_booking = (
                    "insert into room_bookings "
                    "(room_id, check_in_date, check_out_date, first_name, last_name) "
                    "values "
                    "(?, ?, ?, ?, ?);"
                )
                cursor.execute(
                    sql_query_booking,
                    (room_id, check_in, check_out, first_name, last_name),
                )
                return "Комната забронирована", 200
            else:
                for check_in_date, check_out_date in book_rooms:
                    start_date = datetime.strptime(check_in_date, format("%Y%m%d"))
                    end_date = datetime.strptime(check_out_date, format("%Y%m%d"))
                    if (
                        start_date
                        <= datetime.strptime(str(check_in), format("%Y%m%d"))
                        <= end_date
                        or start_date
                        <= datetime.strptime(str(check_out), format("%Y%m%d"))
                        <= end_date
                    ):
                        return "Эту комнату уже забронировали", 409

                sql_query_booking = (
                    "insert into room_bookings"
                    "(room_id, check_in_date, check_out_date, first_name, last_name) "
                    "values "
                    "(?, ?, ?, ?, ?);"
                )
                cursor.execute(
                    sql_query_booking,
                    (room_id, check_in, check_out, first_name, last_name),
                )
                return "Комната забронирована", 200
