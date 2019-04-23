from enum import Enum
import logging
logger = logging.getLogger(__name__)

class DeviceType(Enum):
    DEVNONE = 0
    DHT11 = 1
    LED = 2
    CPUTEMP = 3
    CPUPERCENT = 4
    MEMORY = 5

    def __init__(self, ignored):
        self.__friendly = [
            "None Defined",
            "DHT-11",
            "LED",
            "CPU Temperature",
            "CPU Percentage Used",
            "Memory Information in Bytes"
        ]

    @staticmethod
    def get_type(name):
        if name.upper() == "DHT11":
            return DeviceType.DHT11
        if name.upper() == "LED":
            return DeviceType.LED
        if name.upper() == "CPUTEMP":
            return DeviceType.CPUTEMP
        if name.upper() == "CPUPERCENT" or name.upper() == "CPUPERC":
            return DeviceType.CPUPERCENT
        if name.upper() == "MEMORY":
            return DeviceType.MEMORY
        return DeviceType.DEVNONE

    def get_friendly(self):
        return self.__friendly[self.value]

    def __eq__(self, other):
        return self.value == other.value