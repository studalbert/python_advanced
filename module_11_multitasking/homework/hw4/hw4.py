import queue
import random
import time
from queue import PriorityQueue
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pq = PriorityQueue()


def sleep(arg):
    time.sleep(arg)


class Task:
    def __init__(self, priority, func, args):
        self.priority = priority
        self.func = func
        self.args = args

    # Метод для сравнения объектов по приоритету
    def __lt__(self, other):
        return self.priority < other.priority

    def function(self):
        logger.info(f"Running Task(priority={self.priority})      sleep({self.args})")
        return self.func(self.args)


class Producer(threading.Thread):

    def __init__(self, pq: queue.PriorityQueue, tasks_count: int):
        super().__init__()
        self.pq = pq
        self.tasks_count = tasks_count

    def run(self):
        logger.info("Producer running")
        for i in range(self.tasks_count):
            time_arg = random.uniform(0, 1)
            priority = random.randint(0, 10)
            self.pq.put(Task(priority, sleep, time_arg))
        logger.info("Producer Done")


class Costumer(threading.Thread):

    def __init__(self, pq: queue.PriorityQueue):
        super().__init__()
        self.pq = pq

    def run(self):
        logger.info("Costumer running")
        while not self.pq.empty():
            task = self.pq.get()
            task.function()
            self.pq.task_done()
        logger.info("Consumer: Done")


if __name__ == "__main__":
    tasks_count = 10
    thread_producer = Producer(pq, tasks_count)
    thread_producer.start()
    thread_producer.join()

    thread_costumer = Costumer(pq)
    thread_costumer.start()
    thread_costumer.join()
