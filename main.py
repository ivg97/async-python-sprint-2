from job import Job
from scheduler import Scheduler
from tasks import task_1, task_2, task_3, task_4, task_5

if __name__ == '__main__':

    scheduler = Scheduler()

    job1 = Job(task_1)
    job2 = Job(task_2, max_working_time=2)
    job3 = Job(task_3)
    job4 = Job(task_4)
    job5 = Job(task_5)

    scheduler.add_job(job5)
    scheduler.add_job(job1)
    scheduler.add_job(job2)
    scheduler.add_job(job3)
    scheduler.add_job(job4)

    scheduler.run()
