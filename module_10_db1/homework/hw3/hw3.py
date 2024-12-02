import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()
        result_count = []
        for i in range(1, 4):
            res = cursor.execute(f"SELECT COUNT(*) FROM table_{i}")
            result = res.fetchall()
            result_count.append(result[0][0])
        # 1 задача
        for i in range(len(result_count)):
            print(f"В {i+1} таблице {result_count[i]} строк")

        # 2 задача
        res = cursor.execute("SELECT COUNT(DISTINCT id) from table_1")
        print(f"Уникальных записей в table_1 - {res.fetchall()[0][0]}")

        # 3 задача
        res = cursor.execute(
            "SELECT COUNT(*)"
            "FROM("
            "SELECT * FROM table_1 "
            "INTERSECT "
            "SELECT * FROM table_2) AS intersections"
        )
        result = res.fetchall()
        print(f"{result[0][0]} записей из таблицы table_1 встречается в table_2")

        # 4 задача
        res = cursor.execute(
            "SELECT COUNT(*)"
            "FROM(SELECT * FROM table_1 INTERSECT SELECT * FROM table_2 INTERSECT SELECT * FROM table_3) AS intersections"
        )
        result = res.fetchall()
        print(
            f"{result[0][0]} записей из таблицы table_1 встречается и в table_2, и в table_3"
        )
