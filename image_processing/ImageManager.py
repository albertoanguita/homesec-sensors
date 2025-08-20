from jacpy.object.Singleton import Singleton


# The image manager class handles all camera-related events and commands
class ImageManager(Singleton):
    def __init__(self):
        if not self._initialized:
            self.state = State.STOPPED
            self._initialized = True


    def start(self):
        pass


    def stop(self):
        pass


    def restart(self):
        pass


    def update_param(self, param: str):
        pass