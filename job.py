import datetime
from threading import Timer, Thread
from typing import Callable

from exceptions import ExceptionTime
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
        logger.info(f"Запуск задачи {self.name} {datetime.datetime.now()}")
        try:
            if any(
                    dependenc.status != Status.completed for
                    dependenc in self._dependencies):
                return False

            if ((self._day or self._hour or self._minute)
                    and self._get_run_time() < datetime.datetime.now()):
                return False

            self.status = Status.run
            if self._max_working_time == -1:
                self.target(*self.args, **self.kwargs)
                self.status = Status.completed
            else:
                logger.info(f"Задача {self.name} ограничена временем.")
                try:

                    self.timer = Timer(self._max_working_time, self._stop_timeout)
                    self.timer.start()
                    self.target(*self.args, **self.kwargs)

                except ExceptionTime as err:
                    self.timer.cancel()
                    print(123, err)


            # if self._max_working_time > 0:
            #     logger.info(f"Время выполнения задачи {self.name} истекло!")
            #     self.timer.cancel()
            #     self.status = Status.stop

        except Exception as err:
            logger.error(f"Ошибка при запуске и обрабоки задачи {self.name}: "
                         f"{err}")
            self._retries += 1
            self.status = Status.error

            if self._retries < self._max_retries:
                self.run()
            else:
                logger.warn(f"Не осталось попыток перезапуска задачи! "
                            f"Использовалось попыток: {self._retries}.")
        return self.status == Status.completed

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
        raise ExceptionTime
