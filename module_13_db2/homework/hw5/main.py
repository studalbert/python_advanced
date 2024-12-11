import random
import sqlite3


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:
    cursor.execute("DELETE FROM uefa_commands")
    cursor.execute("DELETE FROM uefa_draw")
    teams_level_for_group = ["strong", "middle", "middle", "low"] * number_of_groups
    number_of_commands = 4 * number_of_groups
    countries = [
        "Russia",
        "Germany",
        "Netherlands",
        "Belgium",
        "United States",
        "Canada",
        "Australia",
        "Japan",
        "India",
        "Brazil",
    ]
    list_for_uefa_commands = [
        (
            "".join(random.sample("abcdefghijklmnopqrstuvwxyz", k=3)),
            random.choice(countries),
            teams_level_for_group[i],
        )
        for i in range(number_of_commands)
    ]
    list_for_uefa_draw = [(i + 1, i // 4 + 1) for i in range(number_of_commands)]
    sql_req1 = """INSERT INTO uefa_commands (command_name, command_country, command_level) VALUES (?, ?, ?);"""
    cursor.executemany(sql_req1, list_for_uefa_commands)
    sql_req2 = """INSERT INTO uefa_draw (command_number, group_number) VALUES (?, ?);"""
    cursor.executemany(sql_req2, list_for_uefa_draw)


if __name__ == "__main__":
    number_of_groups: int = int(input("Введите количество групп (от 4 до 16): "))
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
