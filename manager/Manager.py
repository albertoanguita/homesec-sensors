from jacpy.object.Singleton import Singleton
from numpy.distutils.npy_pkg_config import parse_config

from image_processing.ImageManager import ImageManager
from manager.ManagerCommand import parse_command
# from ManagerCommand import Command, parse_command
from manager.ManagerState import State
from enum import Enum

class Command(Enum):
    START = 1
    STOP = 2
    RESET = 3

# The manager class handles all elements in homesec-sensors. It keeps track
# of the module state and events, and handles incoming requests
class Manager(Singleton):
    def __init__(self):
        if not self._initialized:
            self.state = State.STOPPED
            self.imageManager = ImageManager()
            self._initialized = True


    def get_state(self):
        return self.state

    # todo use a goal based execution framework
    def command(self, commandStr: str) -> bool:
        command = Manager.__parse_command(commandStr)
        if command is not None:
            if self.state == State.STOPPED and (command == Command.START or command == Command.RESET):
                self.state = State.RUNNING_OFF
                self.imageManager.start()

            elif ((self.state == State.RUNNING_OFF or
                   self.state == State.RUNNING_ARMED or
                   self.state == State.RUNNING_ARMING or
                   self.state == State.RUNNING_NIGHT)
                  and command == Command.STOP):
                self.state = State.STOPPED
                self.imageManager.stop()

            return True
        else:
            return False

    @staticmethod
    def __parse_command(commandStr: str) -> Command | None:
        try:
            return Command[commandStr]
        except KeyError:
            return None
    # def command(self, command: object, arguments: object) -> object:
    #     inputCommand = Command(parse_command(command), arguments)
    #     pass


    def image_event(self, event):
        pass