from demo.config.deviceconfig import DeviceConfig
from demo.devices.dht11 import DHT11
import logging
logger = logging.getLogger(__name__)

class DeviceLoader(object):
    def __init__(self):
        self.__devices = []
        self.__switcher={
            1: self.__load_dht11
        }

    def __load_dht11(self, config):
        return DHT11(config)

    def load_devices(self, devices):
        if isinstance(devices, list) == False:
            raise TypeError()
        if len(devices) == 0:
            raise ValueError()

        for device in devices:
            config = DeviceConfig(device)
            logger.debug("Checking Device Config for {}.{}".format(config.Type, config.Name))
            method = self.__switcher.get(config.Type.value)
            logger.debug("Detected Method is {}".format(method))

            if method is not None:
                self.__devices.append(method(config))

    @property
    def Devices(self):
        return self.__devices
