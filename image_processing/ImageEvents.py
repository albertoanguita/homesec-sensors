
"""Interface for image-related events that must be processed by some entity"""
import abc
from abc import abstractmethod

"""Interface for image-related events"""
class ImageEventInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text))

    """The camera system has been successfully initialized"""
    @abstractmethod
    def initialized(self):
        pass

    """The camera system has successfully rebooted"""
    @abstractmethod
    def reboot(self):
        pass

    """The camera system has stopped"""
    @abstractmethod
    def stopped(self):
        pass

    """The camera has detected movement and is now in intense mode"""
    @abstractmethod
    def movement(self):
        pass

    """The camera stopped detecting movement, and is now in standby mode"""
    @abstractmethod
    def no_movement(self):
        pass

    """An unknown person has been detected"""
    @abstractmethod
    def unknown_person(self):
        pass

    """A known person has been detected"""
    @abstractmethod
    def known_person(self):
        pass


