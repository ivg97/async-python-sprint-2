import time
from threading import Lock, Thread

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
        self.__config_file = ConfigFile(file_name=file_name)

        self._threads = None
        self._start_scheduler()
        self._load_configuration()

    def run(self):
        logger.info(f"Старт планировщика...")
        while True:
            running_jobs = [
                job for job in self._jobs if
                job.status == Status.init
            ]
            if len(running_jobs) > self.__pool_size:
                running_jobs = running_jobs[0:self.__pool_size]

            self._threads = [
                Thread(
                    target=job.run
                ) for job in running_jobs
            ]
            if self._threads:

                for thread in self._threads:
                    thread.start()
                else:
                    self._save_configurations()
            time.sleep(1)

    def _start_scheduler(self):
        self._jobs = []
        logger.info(f"Проводятся подготовительные работы..")
        conf_data = self.__config_file.run()
        jobs = conf_data
        logger.info(f"Задачи из конфигурационного файла: {jobs}")

    def restart(self):
        pass

    def stop(self):
        self._stop_scheduler()

    def _stop_scheduler(self):
        pass

    def _load_configuration(self):
        state = self.__config_file.load_status()
        for _job in state:
            if _job["status"] == Status.init.name:
                target = globals().get(_job["target"], None)
                if target:
                    self._jobs.append(
                        Job(name=_job["name"], target=target,)
                    )

    def _save_configurations(self):
        state = [{"name": job.name, "status": job.status.name,
                  "target": job.target.__name__}
                 for job in self._jobs if job._max_working_time == -1]
        self.__config_file.save_status(state)

    def add_job(self,
                job: Job):
        self._jobs.append(job)
        self._save_configurations()
