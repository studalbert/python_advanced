import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
TOTAL_SEATS: int = 50
total_tickets_sold = 0

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        logger.info("Director started work")

    def run(self):
        global TOTAL_TICKETS
        while True:
            if TOTAL_TICKETS == 4:
                with self.sem:
                    TOTAL_TICKETS += 5
                    logger.info("The director added 5 tickets")
            elif total_tickets_sold == TOTAL_SEATS:
                break
        logger.info("The director has finished his work")


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info("Seller started work")

    def run(self) -> None:
        global TOTAL_TICKETS
        global total_tickets_sold
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if total_tickets_sold == TOTAL_SEATS:
                    break
                if TOTAL_TICKETS == 4:
                    self.sem.release()
                    continue
                self.tickets_sold += 1
                total_tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f"{self.name} sold one;  {TOTAL_TICKETS} left")
        logger.info(f"Seller {self.name} sold {self.tickets_sold} tickets")

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    sellers: List[Seller] = []
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)
    director = Director(semaphore)
    director.start()
    for seller in sellers:
        seller.join()


if __name__ == "__main__":
    main()
