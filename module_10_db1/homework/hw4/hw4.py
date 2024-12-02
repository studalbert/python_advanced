import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()

        # 1 задача
        res = cursor.execute("SELECT COUNT(*) FROM salaries WHERE salary < 5000")
        result = res.fetchone()[0]
        print(
            f"{result} человек с острова N находятся за чертой бедности, то есть получает меньше 5000 гульденов в год."
        )

        # 2 задача
        res = cursor.execute("SELECT AVG(salary) FROM salaries")
        result = res.fetchone()[0]
        print(f"средняя зарплата по острову N - {result:.2f}")

        # 3 задача
        res = cursor.execute("SELECT salary FROM salaries ORDER BY salary")
        result = res.fetchall()
        print(f"медианная зарплата по острову - {result[len(result) // 2][0]}")

        # 4 задача. Посчитать число социального неравенства F, определяемое как F = T/K,
        # где T — суммарный доход 10% самых обеспеченных жителей острова N, K —
        # суммарный доход остальных 90% людей. Вывести ответ в процентах с точностью до двух знаков после запятой.

        T_query = cursor.execute(
            "SELECT SUM(salary) FROM(SELECT salary FROM salaries ORDER BY salary DESC LIMIT 0.1 * (SELECT COUNT(*) FROM salaries))"
        )
        T = T_query.fetchone()[0]
        # K_query = cursor.execute(
        #     "SELECT SUM(salary) FROM(SELECT salary FROM salaries ORDER BY salary LIMIT 0.9 * (SELECT COUNT(*) FROM salaries))"
        # )
        K = cursor.execute("SELECT SUM(salary) FROM salaries").fetchone()[0] - T
        F = cursor.execute(f"SELECT CAST(100*ROUND({T/K}, 2) AS DECIMAL)").fetchone()[0]
        print(f"число социального неравенства F = {F}")
