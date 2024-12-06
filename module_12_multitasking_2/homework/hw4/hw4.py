import threading
import time
from queue import Queue, Empty

import requests

url = "http://127.0.0.1:8080/timestamp/"


def func_for_threads(queue):
    for i in range(20):
        # Получаем временную метку
        timestamp = time.time()
        req = requests.get(f"{url}{timestamp}")
        if req.status_code != 200:
            continue
        data = req.text
        queue.put(f"{timestamp} {data}")
        time.sleep(1)


if __name__ == "__main__":
    queue = Queue()
    for i in range(10):
        time.sleep(1)
        thread = threading.Thread(target=func_for_threads, args=(queue,))
        thread.start()

    with open("hw4.log", "w") as file:
        while True:
            try:
                log = queue.get(timeout=1.2)
                queue.task_done()
                file.write(log + "\n")
            except Empty:
                break
