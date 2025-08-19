from jacpy.object.Singleton import Singleton

# from ManagerCommand import Command, parse_command
from manager.ManagerState import State, parse_state


# The manager class handles all elements in homesec-sensors. It keeps track
# of the module state and events, and handles incoming requests
class Manager(Singleton):
    def __init__(self):
        if not self._initialized:
            self.state = State.STOPPED
            self._initialized = True


    def get_state(self):
        return self.state

    def set_state(self, stateStr: str) -> bool:
        state = parse_state(stateStr)
        if state is not None:
            self.state = state
            return True
        else:
            return False


    # def command(self, command: object, arguments: object) -> object:
    #     inputCommand = Command(parse_command(command), arguments)
    #     pass


    def image_event(self, event):
        pass