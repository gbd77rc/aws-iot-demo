from enum import Enum
import logging
logger = logging.getLogger(__name__)

class DeviceType(Enum):
    DEVNONE = 0
    DHT11 = 1
    LED = 2
    CPUTEMP = 3
    CPUPRECENT = 4
    MEMAVAIL = 5
    SERIALNUM = 6

    def __init__(self, ignored):
        self.__friendly = [
            "None Defined",
            "DHT-11 Sensor",
            "LED Light",
            "CPU Temperature",
            "CPU Precentage Used",
            "Memory Available",
            "Serial Number"
        ]

    @staticmethod
    def get_type(name):
        if name.upper() == "DHT11":
            return DeviceType.DHT11
        if name.upper() == "LED":
            return DeviceType.LED
        if name.upper() == "CPUTEMP":
            return DeviceType.CPUTEMP
        if name.upper() == "CPUPRECENT":
            return DeviceType.CPUPRECENT
        if name.upper() == "MEMAVAIL":
            return DeviceType.MEMAVAIL
        if name.upper() == "SERIALNUM":
            return DeviceType.SERIALNUM
        return DeviceType.DEVNONE

    def get_friendly(self):
        return self.__friendly[self.value]

    def __eq__(self, other):
        return self.value == other.value