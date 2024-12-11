import sqlite3


def input_values():
    name: str = input("Введите имя продукта\n>")
    description: str = input("Введите описание продукта\n>")
    amount: str = input("Введите остаток на складе\n>")

    amount_val: int = int(amount)
    return name, description, amount_val


def add_10_records_to_table_warehouse(cursor: sqlite3.Cursor) -> None:
    for i in range(2):
        name, description, amount = input_values()
        cursor.execute(
            """
        INSERT INTO main.table_warehouse (name, description, amount) VALUES (?,?,?)        
        """,
            (name, description, amount),
        )


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_10_records_to_table_warehouse(cursor)
        conn.commit()
