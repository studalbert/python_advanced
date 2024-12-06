from threading import Semaphore, Thread
import time
import sys
import signal

sem: Semaphore = Semaphore()
running = True  # Флаг, который будет управлять работой потоков


def fun1():
    global running
    while running:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    global running
    while running:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)

try:
    t1.start()
    t2.start()
    # Основной поток ждет, пока не будет прерван
    while running:
        time.sleep(0.1)  # Небольшая пауза для уменьшения нагрузки на процессор

except KeyboardInterrupt:
    print("\nReceived keyboard interrupt, quitting threads.")
    running = False  # Прерываем выполнение потока
    t1.join()  # Ждем завершения первого потока
    t2.join()  # Ждем завершения второго потока
    sys.exit(0)
