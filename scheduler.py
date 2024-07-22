import json
import time
from queue import Queue
from threading import Lock

from tasks import *
from file_configuration import ConfigFile
from job import Job
from logger import logger
from schemas import Status


class Scheduler:
    """Планировщик"""
    def __init__(
            self,
            file_name: str = "scheduler_config.json",
            pool_size=10
    ):
        self.__pool_size = pool_size
        self.__lock = Lock()
        self.__config_file = ConfigFile(file_name=file_name)

        # self._jobs = list()
        self._start_scheduler()
        self._load_configuration()
        # print(f"{self._jobs=}")

    def run(self):
        logger.info(f"Старт планировщика...")
        while True:
            running_jobs = [
                job for job in self._jobs if
                job.status == Status.init
            ]
            if len(running_jobs) > self.__pool_size:
                running_jobs = running_jobs[0:10]
            for job in running_jobs:
                if job.status in [
                    Status.init,
                    Status.wait,
                ]:
                    if job.run():
                        print(f'{job.status=}')
                        self._save_configurations()
            time.sleep(1)

    def _start_scheduler(self):
        self._jobs = []
        logger.info(f"Проводятся подготовительные работы..")
        conf_data = self.__config_file.run()
        jobs = conf_data
        # jobs: list = conf_data.get("jobs", [])
        logger.info(f"Задачи из конфигурационного файла: {jobs}")

    def restart(self):
        pass

    def stop(self):
        self._stop_scheduler()

    def _stop_scheduler(self):
        pass

    def _load_configuration(self):
        state = self.__config_file.load_status()
        print(f'{state=}')
        # jobs = state.get("jobs", [])
        for _job in state:
            print(f'{_job=}, {_job["status"]=}')
            print(f"{_job['status'] == 'init'}")
            if _job["status"] == "init":
                target = globals().get(_job["target"], None)
                # print(f"{target=}")
                if target:
                    # print(f"{target=}")
                    self._jobs.append(
                        Job(name=_job["name"], target=target,)
                    )
        print(self._jobs)
            # for job in self._jobs:
            #     if job.name == _job["name"]:
            #         job.status = _job["status"]
            #         self._jobs.append(job)

    def _save_configurations(self):
        logger.info(f"Блокируем..")
        with self.__lock:
            state = [{"name": job.name, "status": job.status.name, "target": job.target.__name__}
                     for job in self._jobs]
        logger.info(f"Разблокировали..")
        self.__config_file.save_status(state)
        print(f'SC {self._jobs=}')

    def add_job(self,
                job: Job):
        logger.info(f"Блокируем..")
        with self.__lock:
            self._jobs.append(job)
        logger.info(f"Разблокировали...")
        self._save_configurations()


