import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {
        "id": 0,
        "title": "A Byte of Python",
        "author": {"id": 1, "first_name": "Swaroop", "last_name": "Chiltur"},
    },
    {
        "id": 1,
        "title": "Moby-Dick; or, The Whale",
        "author": {"id": 2, "first_name": "Herman", "last_name": "Melville"},
    },
    {
        "id": 2,
        "title": "War and Peace",
        "author": {"id": 3, "first_name": "Leo", "last_name": "Tolstoy"},
    },
]

DATABASE_NAME = "table_books.db"
BOOKS_TABLE_NAME = "books"
AUTHORS_TABLE_NAME = "authors"
ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"


@dataclass
class Author:
    first_name: str
    last_name: str
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author: Author
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript(ENABLE_FOREIGN_KEY)
        cursor.execute(
            f"""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
                    """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                                    CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        first_name TEXT,
                                        last_name TEXT
                                    );
                                    """
            )
            cursor.executemany(
                f"""
                            INSERT INTO `{AUTHORS_TABLE_NAME}`
                            (first_name, last_name) VALUES (?, ?)
                            """,
                [
                    (item["author"]["first_name"], item["author"]["last_name"])
                    for item in initial_records
                ],
            )
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author integer not null references authors (id) on delete cascade 
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author) VALUES (?, ?)
                """,
                [(item["title"], item["author"]["id"]) for item in initial_records],
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(
        id=row[0],
        title=row[1],
        author=Author(id=row[3], first_name=row[4], last_name=row[5]),
    )


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM `{BOOKS_TABLE_NAME}` join {AUTHORS_TABLE_NAME} on {BOOKS_TABLE_NAME}.author = {AUTHORS_TABLE_NAME}.id"
        )
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""select * from {AUTHORS_TABLE_NAME} where first_name = ? and last_name = ?""",
            (book.author.first_name, book.author.last_name),
        )
        res = cursor.fetchone()
        if not res:
            cursor.execute(
                f"""
                        INSERT INTO `{AUTHORS_TABLE_NAME}` 
                        (first_name, last_name) VALUES (?, ?)
                        """,
                (book.author.first_name, book.author.last_name),
            )
            book.author.id = cursor.lastrowid
        else:
            book.author.id = res[0]
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, book.author.id),
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` 
            join {AUTHORS_TABLE_NAME} on {BOOKS_TABLE_NAME}.author = {AUTHORS_TABLE_NAME}.id 
            WHERE {BOOKS_TABLE_NAME}.id = ?
            """,
            (book_id,),
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
                    UPDATE {BOOKS_TABLE_NAME}
                    SET title = ?
                    WHERE id = ?
                    """,
            (book.title, book.id),
        )
        book.author.id = cursor.execute(
            f"""SELECT author from {BOOKS_TABLE_NAME} where id = ?""", (book.id,)
        ).fetchone()[0]
        # Обновляем информацию об авторе
        cursor.execute(
            f"""
                    UPDATE {AUTHORS_TABLE_NAME}
                    SET first_name = ?, last_name = ?
                    WHERE id = ?
                    """,
            (book.author.first_name, book.author.last_name, book.author.id),
        )

        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError(
                "No book found with the given ID"
            )  # Генерируем исключение, если книга не найдена


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` join {AUTHORS_TABLE_NAME} on {BOOKS_TABLE_NAME}.author = {BOOKS_TABLE_NAME}.id WHERE title = ?
            """,
            (book_title,),
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def _get_author_obj_from_row(row):
    return Author(id=row[0], first_name=row[1], last_name=row[2])


def get_author_by_id(author_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
        select * from {AUTHORS_TABLE_NAME} where id = ?""",
            (author_id,),
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_author_by_name(first_name, last_name):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
        select * from {AUTHORS_TABLE_NAME} where first_name = ? and last_name = ?""",
            (first_name, last_name),
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""select * from {AUTHORS_TABLE_NAME} where first_name = ? and last_name = ?""",
            (author.first_name, author.last_name),
        )
        res = cursor.fetchone()
        if not res:
            cursor.execute(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}` 
                (first_name, last_name) VALUES (?, ?)
                """,
                (author.first_name, author.last_name),
            )
            author.id = cursor.lastrowid
            return author
        else:
            author.id = res[0]
            return author


def get_books_by_author(author_id) -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * from {BOOKS_TABLE_NAME} "
            f"join {AUTHORS_TABLE_NAME} on {BOOKS_TABLE_NAME}.author={AUTHORS_TABLE_NAME}.id  "
            f"where {AUTHORS_TABLE_NAME}.id = ?",
            (author_id,),
        )
        all_books = cursor.fetchall()
        if all_books:
            return [_get_book_obj_from_row(row) for row in all_books]
        else:
            raise ValueError("No books found for the given author ID.")


def delete_author_by_id(author_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript(ENABLE_FOREIGN_KEY)
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME}
            WHERE id = ?
            """,
            (author_id,),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError(
                "No author found with the given ID"
            )  # Генерируем исключение, если автор не найден
