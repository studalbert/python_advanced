import sqlite3

IVAN_SOVIN_SALARY = 100000


def ivan_sovin_the_most_effective(
    cursor: sqlite3.Cursor,
    name: str,
) -> None:
    cursor.execute(
        "SELECT salary FROM table_effective_manager WHERE name = ?;", (name,)
    )
    salary = cursor.fetchone()[0]
    salary_after_promotion = salary * 1.1
    if salary_after_promotion > IVAN_SOVIN_SALARY:
        cursor.execute("DELETE FROM table_effective_manager WHERE name = ?;", (name,))
    else:
        cursor.execute(
            "UPDATE table_effective_manager SET salary = ? WHERE name = ?;",
            (salary_after_promotion, name),
        )


if __name__ == "__main__":
    name: str = input("Введите имя сотрудника: ")
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
