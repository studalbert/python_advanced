import sqlite3


def get_number_of_lucky_days(c: sqlite3.Cursor, month_number: int) -> float:
    start_date = f"2023-{month_number}-01"
    if month_number == 12:
        end_date = f"2024-01-01"  # Январь следующего года
    else:
        end_date = f"2023-{month_number + 1}-01"
    sql_req = "SELECT * FROM table_green_future WHERE date >= ? and date < ?"
    res_list = c.execute(sql_req, (start_date, end_date)).fetchall()
    dct = {}
    for id, date, action in res_list:
        dct[date] = {}


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        percent_of_lucky_days = get_number_of_lucky_days(cursor, 12)
        # print(f"В декабре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
