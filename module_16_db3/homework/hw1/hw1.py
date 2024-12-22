import sqlite3

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"

CREATE_DIRECTOR_TABLE = """
drop table if exists 'director';
create table 'director' (
    dir_id integer primary key autoincrement,
    dir_first_name varchar(50),
    dir_last_name varchar(50)
)
"""

CREATE_ACTORS_TABLE = """
drop table if exists 'actors';
create table 'actors' (
    act_id integer primary key autoincrement,
    act_first_name varchar(50),
    act_last_name varchar(50),
    act_gender varchar(1)
)
"""

CREATE_MOVIE_TABLE = """
drop table if exists 'movie';
create table 'movie' (
    mov_id integer primary key autoincrement,
    mov_title varchar(50)
)
"""

CREATE_MOVIE_CAST_TABLE = """
drop table if exists 'movie_cast';
create table 'movie_cast' (
    act_id integer not null references actors (act_id) on delete cascade,
    mov_id integer not null references movie (mov_id),
    role varchar(50)
)
"""

CREATE_MOVIE_DIRECTION_TABLE = """
drop table if exists 'movie_direction';
create table 'movie_direction' (
    dir_id integer not null references director (dir_id) on delete cascade,
    mov_id integer not null references movie (mov_id)
)
"""

CREATE_OSCAR_AWARDED_TABLE = """
drop table if exists 'oscar_awarded';
create table 'oscar_awarded' (
    award_id integer primary key autoincrement,
    mov_id integer not null references movie (mov_id) on delete cascade
)
"""

if __name__ == "__main__":
    with sqlite3.connect("hw1.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(ENABLE_FOREIGN_KEY)
        cursor.executescript(CREATE_DIRECTOR_TABLE)
        cursor.executescript(CREATE_MOVIE_TABLE)
        cursor.executescript(CREATE_ACTORS_TABLE)
        cursor.executescript(CREATE_MOVIE_CAST_TABLE)
        cursor.executescript(CREATE_MOVIE_DIRECTION_TABLE)
        cursor.executescript(CREATE_OSCAR_AWARDED_TABLE)
