from demo.devices.devicetype import DeviceType
from demo.config.deviceconfig import DeviceConfig
from demo.devices.directiontype import DirectionType
import logging
logger = logging.getLogger(__name__)


class DeviceBase:
    def __init__(self, config, type, direction = DirectionType.IN):
        if isinstance(config, DeviceConfig) == False:
            raise TypeError()
        if isinstance(type, DeviceType) == False:
            raise TypeError()

        if isinstance(direction, DirectionType) == False:
            raise TypeError()

        if type != config.Type:
            raise ValueError()
        self.__config = config
        self.__direction = direction

    @property
    def Config(self):
        return self.__config

    @property
    def Direction(self):
        return self.__direction

    def read(self):
        raise NotImplementedError()

    def write(self, value):
        raise NotImplementedError()
    
