from jacpy.io.baseIniConfig import BaseIniConfig


class PathsConfig(BaseIniConfig):

    __CONFIG = 'CONFIG'

    def __init__(self):
        super().__init__('config.ini')

    def faces_path(self) -> str:
        return self._get_str_value(self.__CONFIG, 'facesPath')

    def facenet_weights(self) -> str:
        return self._get_str_value(self.__CONFIG, 'facenetWeights')

    def encodings_path(self) -> str:
        return self._get_str_value(self.__CONFIG, 'encodingsPath')


class ParamsConfig(BaseIniConfig):
    __CONFIG = 'PARAMS'

    def __init__(self):
        super().__init__('config.ini')

    def threshold(self) -> float:
        return self._get_float_value(self.__CONFIG, 'threshold')

    def set_threshold(self, value: float) -> None:
        self._set_value(self.__CONFIG, 'threshold', value)

    def arm_time_seconds(self) -> int:
        return self._get_int_value(self.__CONFIG, 'arm-time-seconds')

    def set_arm_time_seconds(self, value: int) -> None:
        self._set_value(self.__CONFIG, 'arm-time-seconds', value)
