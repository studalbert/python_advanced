import sqlite3
from datetime import datetime, timedelta


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    cursor.execute("delete from table_friendship_schedule")
    sport_weekday_dct = {
        "футбол": 0,
        "хоккей": 1,
        "шахматы": 2,
        "SUP сёрфинг": 3,
        "бокс": 4,
        "Dota2": 5,
        "шах-бокс": 6,
    }
    sql_req_employees = (
        """select id, preferable_sport from table_friendship_employees"""
    )

    sql_req_schedule = (
        """insert into table_friendship_schedule (employee_id, date) VALUES (?, ?);"""
    )
    start_date = datetime(2020, 1, 1)
    result = cursor.execute(sql_req_employees).fetchall()
    for i in range(366):
        date = start_date + timedelta(days=i)
        weekday_number = date.weekday()
        # Преобразуем в строку в формате YYYY-MM-DD
        date_string = date.strftime("%Y-%m-%d")
        res_list = []
        k = i
        while True:
            id, sport = result[k % 366]
            if sport_weekday_dct[sport] == weekday_number:
                k += 1
                continue
            else:
                res_list.append((id, date_string))
                k += 1
            if len(res_list) == 10:
                break

        cursor.executemany(sql_req_schedule, res_list)


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
