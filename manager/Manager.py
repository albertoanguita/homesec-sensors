import logging
from enum import Enum

import requests
from jacpy.object.Singleton import Singleton
from jacpy.time import TimeUtil

from image_processing.ImageManager import ImageManager
from manager.ImageEventImpl import ImageEventImpl
# from ManagerCommand import Command, parse_command
from manager.ManagerState import State


class Command(Enum):
    START = 1
    STOP = 2
    RESET = 3


UNKNOWN_PERSON_EVENT = 'unknown_person_detected'
KNOWN_PERSON_EVENT = 'known_person_detected'

# The manager class handles all elements in homesec-sensors. It keeps track
# of the module state and events, and handles incoming requests
class Manager(Singleton):
    def __init__(self):
        if not self._initialized:
            self.state = State.STOPPED
            self.callback_url = None
            self.imageManager = ImageManager(ImageEventImpl(self))

            logging.config.fileConfig('logging.ini', encoding='UTF-8')
            self.logger = logging.getLogger(__name__)
            self.logger.info('Manager start')

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


    def set_callback_url(self, callback_url: str) -> None:
        if callback_url is not None:
            self.callback_url = callback_url
            self.logger.info('Callback URL set to: {}'.format(callback_url))


    def unknown_person_detected(self):
        # todo initiate protocol
        if self.callback_url is not None:
            requests.post(self.callback_url, self.build_request_data(UNKNOWN_PERSON_EVENT))
        else:
            self.logger.info('Callback URL not set. Cannot report unknown person detected.')


    def known_person_detected(self):
        # todo initiate protocol
        if self.callback_url is not None:
            requests.post(self.callback_url, self.build_request_data(KNOWN_PERSON_EVENT))
        else:
            self.logger.info('Callback URL not set. Cannot report known person detected.')


    @staticmethod
    def build_request_data(event: str) -> dict:
        return {'timestamp': TimeUtil.current_milli_time(), 'event_type': event}