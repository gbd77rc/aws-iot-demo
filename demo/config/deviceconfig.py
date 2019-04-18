from demo.devices.devicetype import DeviceType
import logging
logger = logging.getLogger(__name__)


# {
#     "type": "led",        // Mandatory
#     "name": "Green",      // Mandatory
#     "pin": 26,            // Optional
#     "location": ""        // Optional if pin specified then this is not allowed
# }

class DeviceConfig:
    def __init__(self, config):
        # check if an object or not
        if isinstance(config, dict) == False:
            raise TypeError()

        try:
            self.__name = config["name"]
            self.__type = DeviceType.get_type(config["type"])
            if self.__type == DeviceType.DEVNONE:
                raise ValueError()
            self.__name = "{} ({})".format(self.__name, self.__type.get_friendly())
        except KeyError:
            raise ValueError()

        self.__pin = 0
        self.__location = config["location"] if "location" in config else ""

        # check if we are an external device connected to a pin
        if "pin" in config:
            self.__pin = config["pin"]
            self.__location = ""

    @property
    def Name(self):
        return self.__name

    @property
    def Type(self):
        return self.__type

    @property
    def Pin(self):
        return self.__pin

    @property
    def Location(self):
        return self.__location