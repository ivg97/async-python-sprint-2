import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Process

from job import Job
from scheduler import Scheduler
from tasks import task_1, task_2


def task():
    time.sleep(5)
    print("Task is running")


if __name__ == '__main__':

    scheduler = Scheduler()
    # job1 = Job(task_1)
    # job2 = Job(task_1)
    # job3 = Job(task_1)
    # job4 = Job(task_1)
    # job5 = Job(task_1)
    job6 = Job(task_2, max_working_time=2)
    # job7 = Job(task_2)
    # job8 = Job(task_2)
    # job9 = Job(task_2)
    # job10 = Job(task_2)
    # scheduler.add_job(job1)
    # scheduler.add_job(job2)
    # scheduler.add_job(job3)
    # scheduler.add_job(job4)
    # scheduler.add_job(job5)
    scheduler.add_job(job6)
    # scheduler.add_job(job7)
    # scheduler.add_job(job8)
    # scheduler.add_job(job9)
    # scheduler.add_job(job10)
    # job = Job(print, args=("print",),)
    # jobs = [Job(print, args=(f"print_{i}",)) for i in range(15)]
    # for i in jobs:
    #     scheduler.add_job(i)
    # with ProcessPoolExecutor() as pool:
    scheduler.run()
    # time.sleep(5)
    # print('time')
    # scheduler.stop()
    # scheduler_thread = threading.Thread(target=scheduler.run)
    # scheduler_thread.start()
    # # time.sleep(2)
    # scheduler_thread.join()
