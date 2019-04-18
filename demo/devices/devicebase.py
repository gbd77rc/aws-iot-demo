from demo.devices.devicetype import DeviceType
from demo.config.deviceconfig import DeviceConfig
import logging
logger = logging.getLogger(__name__)


class DeviceBase:
    def __init__(self, config):
        if isinstance(config, DeviceConfig) == False:
            raise TypeError()
        self.__config = config

    @property
    def Config(self):
        return self.__config

    def read(self):
        raise NotImplementedError()

    def write(self, value):
        raise NotImplementedError()
    
