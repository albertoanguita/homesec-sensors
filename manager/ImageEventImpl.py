from image_processing.ImageEvents import ImageEventInterface
from manager.Manager import Manager
import logging
import logging.config

class ImageEventImpl(ImageEventInterface):
    def __init__(self, manager: Manager):
        self.manager = manager
        logging.config.fileConfig('logging.ini', encoding='UTF-8')
        self.logger = logging.getLogger(__name__)
        self.logger.info('ImageEventImpl start')

    def initialized(self):
        self.logger.info('ImageEventImpl initialized')

    def reboot(self):
        pass

    def stopped(self):
        pass

    def movement(self):
        pass

    def no_movement(self):
        pass

    def unknown_person(self):
        self.logger.warning('ImageEventImpl unknown_person')
        self.manager.unknown_person_detected()
        pass

    def known_person(self):
        self.logger.warning('ImageEventImpl known_person')
        self.manager.known_person_detected()
        pass
