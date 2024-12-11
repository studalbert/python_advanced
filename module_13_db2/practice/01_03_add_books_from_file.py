import sqlite3
import csv


def add_books_from_file(c: sqlite3.Cursor, file_name: str) -> None:
    insert_query = """INSERT INTO table_books (book_name, author, publish_year, ISBN) VALUES (?,?,?,?)"""
    # Открываем CSV-файл и читаем его построчно
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if len(row) < 4:
                continue
            book_name = row[1]
            author = row[2]
            publish_year = int(row[3])
            isbn = row[0]
            c.execute(insert_query, (book_name, author, publish_year, isbn))


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_books_from_file(cursor, "book_list.csv")
        conn.commit()
