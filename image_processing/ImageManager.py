from enum import Enum

from jacpy.object.Singleton import Singleton

from image_processing.ImageEvents import ImageEventInterface
from image_processing.camera.HomeSecurity import CameraDetector


# The image manager class handles all camera-related events and commands
class ImageManager(Singleton):
    def __init__(self):
        if not self._initialized:
            self.state = State.STOPPED
            self.camera_detector = None
            self._initialized = True


    def initialize(self, image_events: ImageEventInterface):
        if self.camera_detector is None:
            self.camera_detector = CameraDetector().initialize(image_events)
        return self


    def start(self):
        self.camera_detector.start()
        pass


    def stop(self):
        self.camera_detector.stop()
        pass


    def restart(self):
        # todo
        pass


    def update_param(self, param: str):
        # todo
        pass


    def get_latest_frame(self):
        pass



class State(Enum):
    STOPPED = 1
    RUNNING = 2