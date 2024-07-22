import threading
import time

from job import Job
from scheduler import Scheduler


def task():
    time.sleep(5)
    print("Task is running")


if __name__ == '__main__':

    scheduler = Scheduler()
    job = Job(task)
    scheduler.add_job(job)
    # job = Job(print, args=("print",),)
    # jobs = [Job(print, args=(f"print_{i}",)) for i in range(15)]
    # for i in jobs:
    #     scheduler.add_job(i)

    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()

    scheduler_thread.join()
