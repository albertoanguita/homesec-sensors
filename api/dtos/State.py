from dataclasses import dataclass
from enum import Enum


class State:
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4



@dataclass(frozen=True)
class StateDto:
    state: int
