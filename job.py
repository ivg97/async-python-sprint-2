import datetime
import time
from threading import Timer
from typing import Callable

from logger import logger
from schemas import Status


class Job:
    def __init__(self,
                 target: Callable,
                 name: str | None = None,
                 day=None,
                 hour=None,
                 minute=None,
                 max_working_time=-1,
                 max_retries=1,
                 dependencies: list | None = None,
                 args: tuple = None,
                 kwargs: dict = None):

        self.target = target
        self.name = name if name else (f"{self.__class__.__name__}_"
                                       f"{self.__class__.__hash__(self)}")
        self.status: Status = Status.init
        self.args = args if args else tuple()
        self.kwargs = kwargs if kwargs else {}

        self._day = day
        self._hour = hour
        self._minute = minute
        self._max_working_time = max_working_time
        self._max_retries = max_retries - 1
        self._retries = 0
        self._dependencies = dependencies if isinstance(
            dependencies,
            list
        ) else []
        logger.info(f"Инициализация задачи {self.name}")

    def run(self):
        logger.info(f"Запуск задачи {self.name}")
        try:
            if any(
                    dependenc.status != Status.completed for
                    dependenc in self._dependencies):
                print(1)
                return False

            if ((self._day or self._hour or self._minute)
                    and self._get_run_time() < datetime.datetime.now()):
                print(2)
                return False

            self.status = Status.run
            print(3, self.status.name)
            if self._max_working_time > 0:
                logger.info(f"Задача {self.name} ограничена временем.")
                print(4)
                self.timer = Timer(self._max_working_time, self._stop_timeout)
                self.timer.start()
            print(5)

            self.target(*self.args, **self.kwargs)
            self.status = Status.completed

            print(6, self.status.name)
            if self._max_working_time > 0:
                logger.info(f"Время выполнения задачи {self.name} истекло!")
                self.timer.cancel()
                self.status = Status.stop

        except Exception as err:
            logger.error(f"Ошибка при запуске и обрабоки задачи {self.name}: "
                         f"{err}")
            self._retries += 1
            self.status = Status.error

        if self._retries < self._max_retries:
            print(f'{self._retries=}, {self._max_retries}')
            print(7, self.status.name)
            self.run()
        else:
            logger.warn(f"Не осталось попыток перезапуска задачи! "
                        f"Использовалось попыток: {self._retries}.")

        print(8, self.status.name)
        print(self.status == Status.completed)
        return self.status == Status.completed

    # def _run_task(self):
    #     try:
    #         self.target(*self.args, **self.kwargs)
    #         self.status = Status.completed
    #     except Exception as err:
    #         logger.error(f"Ошибка при выполнении задачи {self.name}: "
    #                      f"{err}")
    #         self.status = Status.error

    def pause(self):
        try:
            self.status = Status.wait
        except Exception as err:
            pass

    def stop(self):
        try:
            self.status = Status.stop
        except Exception as err:
            pass

    def _get_run_time(self):
        now_time = datetime.datetime.now()
        day = self._day if self._day else 0
        hour = self._hour if self._hour else 0
        minute = self._minute if self._minute else 0
        td = datetime.timedelta(days=day, hours=hour, minutes=minute)
        return now_time + td

    def _stop_timeout(self):
        if self.status == Status.run:
            self.status = Status.timeout_stop
