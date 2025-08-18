
class CommandType:
    START = 0
    STOP = 1
    RESET = 2
    GET_STATUS = 3
    SET_MODE = 4


class Command:
    def __init__(self, command: CommandType, arguments: object):
        self.command = command
        self.arguments = arguments

    def validate_arguments(self) -> bool:
        if self.command is None:
            return False

        match self.command:
            case CommandType.START | CommandType.STOP | CommandType.RESET | CommandType.GET_STATUS:
                return True

            case CommandType.SET_MODE:
                return True if self.arguments["mode"] is not None else False

            case _:
                return False


