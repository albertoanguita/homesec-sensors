from image_processing.ImageEvents import ImageEventInterface
from manager.Manager import Manager


class ImageEventImpl(ImageEventInterface):
    def __init__(self, manager: Manager):
        self.manager = manager

    def initialized(self):
        pass

    def reboot(self):
        pass

    def stopped(self):
        pass

    def movement(self):
        pass

    def no_movement(self):
        pass

    def unknown_person(self):
        pass

    def known_person(self):
        pass
