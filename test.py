import requests

from job_2 import Job
from scheduler_2 import scheduler


def create_file_task():
    print('create')
    with open('example.txt', 'w') as f:
        f.write('Hello, World!')

def read_file_task():
    with open('example.txt', 'r') as f:
        print(f.read())

def network_task():
    print('network')
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    print(response.json())

job4 = Job(id="4", action=create_file_task)
job5 = Job(id="5", action=read_file_task, dependencies=[job4])
job6 = Job(id="6", action=network_task, dependencies=[job5])

scheduler.add_job(job4)
scheduler.add_job(job5)
scheduler.add_job(job6)