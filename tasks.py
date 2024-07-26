"""
Модуль для хранения всех задач
"""
import json
import time

import requests

from logger import logger


def task_1(*args, **kwargs):
    logger.info(f"Выполнение задачи 1")
    time.sleep(2)
    print("Task 1 is running")


def task_2(*args, **kwargs):
    logger.info(f"Выполнение задачи 2")
    time.sleep(7)
    print("Task 2 is running")


def task_3(*args, **kwargs):
    logger.info(f"Выполнение задачи 3: write file")
    with open('test_3.txt', 'w', encoding="utf-8") as f:
        json.dump("Example text", f)
    print(f"Task 3 is running")


def task_4(*args, **kwargs):
    logger.info(f"Выполнение задачи 4: read file")
    with open('test_3.txt', 'r', encoding="utf-8") as f:
        result = json.load(f)
    print(f"Task 4 is running: {result}")


def task_5(*args, **kwargs):
    logger.info(f"Выполнение задачи 5: network request")
    response = requests.get("https://practicum.yandex.ru/")
    print(f"Task 5 is running: {response.status_code}")
