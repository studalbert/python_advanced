import threading
import time
import requests
import logging
import sqlite3


URL = "https://swapi.dev/api/people/{}/"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_save_info(URL):
    req = requests.get(URL)
    if req.status_code != 200:
        return
    data = req.json()
    name_p, age_p, gender_p = data["name"], data["birth_year"], data["gender"]
    with sqlite3.connect("module10_hw2.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO star_wars_people (name, birth_year, gender) VALUES (?, ?, ?)",
            (name_p, age_p, gender_p),
        )


def load_sequental():
    start = time.time()
    for i in range(1, 21):
        get_save_info(URL.format(i))
    logger.info("load_sequental() done in {:.4}".format(time.time() - start))


def load_multithreading():
    start = time.time()
    threads = []
    for i in range(1, 21):
        thread = threading.Thread(target=get_save_info, args=(URL.format(i),))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    logger.info("load_multithreading() done in {:.4}".format(time.time() - start))


if __name__ == "__main__":
    load_sequental()
    load_multithreading()
