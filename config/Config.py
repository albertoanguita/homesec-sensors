from jacpy.io.baseIniConfig import BaseIniConfig


# todo turn into singleton
class Config(BaseIniConfig):

    __CONFIG = 'CONFIG'

    def __init__(self):
        super().__init__('config.ini')

    def faces_path(self) -> str:
        return self._get_str_value(self.__CONFIG, 'facesPath')

    def facenet_weights(self) -> str:
        return self._get_str_value(self.__CONFIG, 'facenetWeights')

    def encodings_path(self) -> str:
        return self._get_str_value(self.__CONFIG, 'encodingsPath')


