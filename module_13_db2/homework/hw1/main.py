import sqlite3
import sys


def check_if_vaccine_has_spoiled(cursor: sqlite3.Cursor, truck_number: str) -> bool:
    # Проверка существования такого номера грузовика
    sql_req_exists = """SELECT EXISTS(SELECT 1 FROM  table_truck_with_vaccine WHERE truck_number = ?);"""
    cursor.execute(sql_req_exists, (truck_number,))
    res = cursor.fetchone()[0]
    if res:
        sql_req = """select count(1) from table_truck_with_vaccine 
        where truck_number = ? and temperature_in_celsius not between 16 and 20"""
        cursor.execute(sql_req, (truck_number,))
        result = cursor.fetchone()[0]
        if result >= 3:
            return True
        else:
            return False
    else:
        print("Нет такого грузовика в БД")
        sys.exit(0)


if __name__ == "__main__":
    truck_number: str = input("Введите номер грузовика: ")
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print("Испортилась" if spoiled else "Не испортилась")
        conn.commit()
