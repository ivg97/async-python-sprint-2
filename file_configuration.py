import json

from logger import logger


class ConfigFile:
    """Работа с конфигурационным файлом"""
    def __init__(
            self,
            file_name: str = "scheduler_config.json"
    ):
        self.__conf_file: str = file_name

    def run(self):
        logger.info(f"Проверка конфигурационного файла..")
        file_data = self.__read_config()
        if not file_data:
            start_data = self.__created_conf_file()
            return start_data
        return file_data

    def save_status(self, state):
        with open(self.__conf_file, "w", encoding="utf-8") as f:
            json.dump(state, f)

    def load_status(self):
        with open(self.__conf_file, "r", encoding="utf-8") as f:
            state = json.load(f)
            return state

    def __read_config(self):
        try:
            with open(self.__conf_file, encoding="utf-8") as f:
                data = f.read()
                return json.loads(data)
        except (FileNotFoundError, json.JSONDecodeError):
            logger.info(f"Конфигурацинный файл отсутствует.. Создаем..")
            return self.__created_conf_file()

    def __write_config(self, write_data):
        with open(self.__conf_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(write_data))

    def __created_conf_file(self):
        with open(self.__conf_file, 'w', encoding="utf-8") as f:
            conf_info = {

            }
            logger.info(f"Создали конфигурационный файл с "
                        f"настройками: {conf_info}")
            f.write(json.dumps(conf_info))
            return conf_info


_conf_info = {
                "jobs": [
                    {
                        "job1": "run",
                    },
                    {
                        "job2": "wait"
                    }
                ]
            }