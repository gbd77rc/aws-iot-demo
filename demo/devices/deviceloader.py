from demo.config.deviceconfig import DeviceConfig
from demo.devices.dht11 import DHT11
from demo.devices.led import Led
from demo.devices.cpu_precent import CpuPercent
from demo.devices.linux_cpu_temp import CpuTemp
from demo.devices.memory_load import MemoryInfo

import logging
logger = logging.getLogger(__name__)

class DeviceLoader(object):
    def __init__(self):
        self.__devices = []
        self.__switcher={
            1: self.__load_dht11,
            2: self.__load_led,
            3: self.__load_cpu_t,
            4: self.__load_cpu_p,
            5: self.__load_memory
        }

    def __load_dht11(self, config):
        return DHT11(config)

    def __load_led(self, config):
        return Led(config)

    def __load_cpu_p(self, config):
        return CpuPercent(config)        

    def __load_cpu_t(self, config):
        return CpuTemp(config)

    def __load_memory(self, config):
        return MemoryInfo(config)        

    def load_devices(self, devices):
        if isinstance(devices, list) == False:
            raise TypeError()
        if len(devices) == 0:
            raise ValueError()

        for device in devices:
            config = device
            if isinstance(device, DeviceConfig) == False:
                config = DeviceConfig(device)
            logger.debug("Checking Device Config for {}.{}".format(config.Type, config.Name))
            method = self.__switcher.get(config.Type.value)
            logger.debug("Detected Method is {}".format(method))

            if method is not None:
                self.__devices.append(method(config))

    @property
    def Devices(self):
        return self.__devices
