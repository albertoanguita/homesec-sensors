from enum import Enum

class State(Enum):
    STOPPED = 1
    STOPPING = 2
    STARTING = 3
    RUNNING_OFF = 4
    RUNNING_ARMING = 5
    RUNNING_ARMED = 6
    RUNNING_NIGHT = 7


def parse_state(stateStr: str) -> State | None:
    try:
        return State[stateStr]
    except KeyError:
        return None