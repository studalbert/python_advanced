from datetime import datetime, timezone
import sqlite3


def log_bird(
    cursor: sqlite3.Cursor,
    bird_name: str,
    date_time: str,
) -> None:
    sql_req = """INSERT INTO table_birds (bird_name, date_time) VALUES (?,?);"""
    cursor.execute(sql_req, (bird_name, date_time))


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    sql_req = """SELECT EXISTS(SELECT 1 FROM table_birds WHERE bird_name = ?);"""
    cursor.execute(sql_req, (bird_name,))
    result = cursor.fetchone()[0]
    if result:
        return True
    else:
        return False


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        try:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS table_birds "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "bird_name TEXT NOT NULL, "
                "date_time TEXT NOT NULL);"
            )
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")
        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
        connection.commit()
