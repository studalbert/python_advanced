import multiprocessing
import time
import requests
import logging
import sqlite3
from multiprocessing.pool import ThreadPool

URL = "https://swapi.dev/api/people/{}/"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_save_info(URL):
    try:
        req = requests.get(URL)
        if req.status_code != 200:
            return
        data = req.json()
        name_p, age_p, gender_p = data["name"], data["birth_year"], data["gender"]
        save_info_in_db(name_p, age_p, gender_p)
    except requests.exceptions.ConnectionError:
        return


def save_info_in_db(name, age, gender):
    with sqlite3.connect("module11_hw1.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO star_wars_people (name, birth_year, gender) VALUES (?, ?, ?)",
            (name, age, gender),
        )


def task_execution_with_threadpool():
    start = time.time()
    pool = ThreadPool(processes=20)
    result = pool.map(get_save_info, [URL.format(i) for i in range(1, 21)])
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f"Time taken in seconds with threadpool - {end - start}")


def task_execution_with_processpool():
    start = time.time()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    result = pool.map(get_save_info, [URL.format(i) for i in range(1, 21)])
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f"Time taken in seconds with processes pool - {end - start}")


if __name__ == "__main__":
    with sqlite3.connect("module11_hw1.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS star_wars_people (
        name VARCHAR(100), birth_year VARCHAR(20), gender VARCHAR(10)
        )
        """
        )
        conn.commit()
    task_execution_with_threadpool()
    task_execution_with_processpool()
