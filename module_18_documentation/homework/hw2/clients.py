from multiprocessing.pool import ThreadPool
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url: str = "http://0.0.0.0:5000/api/books"


class BookClient:
    URL: str = "http://0.0.0.0:5000/api/books"
    TIMEOUT: int = 5
    URL_AUTHORS = "http://0.0.0.0:5000/api/authors"

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(
                "Wrong params. Response message: {}".format(response.json())
            )

    def get_book_by_id(self, id: int):
        response = self.session.get(f"{self.URL}/{id}", timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                "Wrong params. Response message: {}".format(response.json())
            )

    def put_book_by_id(self, id: int, data: dict):
        response = self.session.put(f"{self.URL}/{id}", json=data, timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                "Wrong params. Response message: {}".format(response.json())
            )

    def delete_book_by_id(self, id: int):
        response = self.session.delete(f"{self.URL}/{id}", timeout=self.TIMEOUT)
        if response.status_code == 204:
            return
        else:
            raise ValueError(
                "Wrong params. Response message: {}".format(response.json())
            )

    def get_books_by_author(self, id):
        response = self.session.get(f"{self.URL_AUTHORS}/{id}", timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                "Wrong params. Response message: {}".format(response.json())
            )

    def delete_author_by_id(self, id):
        response = self.session.delete(f"{self.URL_AUTHORS}/{id}", timeout=self.TIMEOUT)
        if response.status_code == 204:
            return
        else:
            raise ValueError(
                "Wrong params. Response message: {}".format(response.json())
            )

    def add_new_author(self, data: dict):
        response = self.session.post(self.URL_AUTHORS, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(
                "Wrong params. Response message: {}".format(response.json())
            )


def task():
    response = requests.get(url)
    return response.json()


class RequestsOnApi:
    client = BookClient()

    def responses_without_threadpool_session(self, count_req: int):
        start = time.time()
        for i in range(count_req):
            self.client.get_all_books()
        end = time.time()
        logger.info(
            f"Время выполнения {count_req} запросов без использования пула потоков и с использованием сессии = {end - start}"
        )

    def responses_with_threadpool_session(self, count_req: int):
        pool = ThreadPool(processes=10)
        start = time.time()
        result = pool.map(lambda _: self.client.get_all_books(), range(count_req))
        pool.close()
        pool.join()
        end = time.time()
        logger.info(
            f"Время выполнения {count_req} запросов с использованием пула потоков и с использованием сессии = {end - start:.2f} секунд"
        )

    def responses_without_threadpool_not_session(self, count_req: int):
        start = time.time()
        for i in range(count_req):
            response = requests.get(url, timeout=5)
            res = response.json()
        end = time.time()
        logger.info(
            f"Время выполнения {count_req} запросов без использования пула потоков и без использования сессии = {end - start}"
        )

    def responses_with_threadpool_not_session(self, count_req: int):
        pool = ThreadPool(processes=10)
        start = time.time()
        result = pool.map(lambda _: task(), range(count_req))
        pool.close()
        pool.join()
        end = time.time()
        logger.info(
            f"Время выполнения {count_req} запросов с использованием пула потоков и без использования сессии = {end - start:.2f} секунд"
        )


if __name__ == "__main__":
    # # 10 запросов
    # req = RequestsOnApi()
    # req.responses_without_threadpool_session(10)
    # req.responses_with_threadpool_session(10)
    # req.responses_without_threadpool_not_session(10)
    # req.responses_with_threadpool_not_session(10)
    # # 100 запросов
    # req = RequestsOnApi()
    # req.responses_without_threadpool_session(100)
    # req.responses_with_threadpool_session(100)
    # req.responses_without_threadpool_not_session(100)
    # req.responses_with_threadpool_not_session(100)
    # # 1000 запросов
    req = RequestsOnApi()
    req.responses_without_threadpool_session(1000)
    req.responses_with_threadpool_session(1000)
    req.responses_without_threadpool_not_session(1000)
    req.responses_with_threadpool_not_session(1000)
