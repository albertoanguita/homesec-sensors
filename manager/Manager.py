from ManagerCommand import Command


# The manager class handles all elements in homesec-sensors. It keeps track
# of the module state and events, and handles incoming requests
class Manager:
    def __init__(self):
        self.state = None

    def command(self, command: Command):
        pass


    def image_event(self, event):
        pass