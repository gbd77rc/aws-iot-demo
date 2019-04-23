import logging
logger = logging.getLogger(__name__)

from demo.config.usecaseconfig import UseCaseConfig
from demo.devices.devicebase import DeviceBase

class UseCase:
    def __init__(self, config):
        if isinstance(config, UseCaseConfig) == False:
            raise TypeError()
        self.__config = config
        self.__devices = []

    @property
    def Config(self):
        return self.__config

    @property
    def Devices(self):
        return self.__devices

    def load_devices(self, devices):
        if isinstance(devices, list) == False:
            raise ValueError()
        
        for device in devices:
            logger.debug("Device being checked is [{}]".format(device))
            if isinstance(device, DeviceBase) == False:
                raise ValueError()

            for name in self.__config.DeviceNames:
                logger.debug("Device Name is [{}]".format(name))
                if name == device.Config.Name:
                    self.__devices.append(device)

        



        