import logging
logger = logging.getLogger(__name__)


# {
#     "use-case": "Engineering",
#     "push": 10,
#     "payload-type": "JSON",
#     "devices": ["DHT-11", "CPU Temperature", "CPU Precentage", "Memory Available", "Serial Number", "Green", "Yellow", "Red"]
# }

class UseCaseConfig:
    def __init__(self, config):
        # check if an object or not
        if isinstance(config, dict) == False:
            raise TypeError()

        try:
            self.__name = config["use-case"]
            if self.__name == "":
                raise ValueError()

            self.__wait = config["push"] if config["push"] > 0 else 1
            self.__payload = config["payload-type"].upper()
            if self.__payload != "JSON" and self.__payload != "PROTOBUF":
                raise ValueError()
            
            self.__devicenames = config["devices"]
            if len(self.__devicenames) == 0:
                raise ValueError()

        except KeyError:
            raise ValueError()

    @property
    def Name(self):
        return self.__name

    @property
    def Payload(self):
        return self.__payload

    @property
    def Wait(self):
        return self.__wait

    @property
    def DeviceNames(self):
        return self.__devicenames