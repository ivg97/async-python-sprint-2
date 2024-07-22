from enum import Enum


class Status(Enum):
    run = "run"
    wait = "wait"
    error = "error"
    stop = "stop"
    completed = "completed"
    init = "init"
    timeout_stop = "timeout_stop"
