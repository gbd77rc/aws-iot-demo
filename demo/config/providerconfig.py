import logging
logger = logging.getLogger(__name__)


# "type": "aws",
# "client_id": "rpi-1",
# "thing_id": "iot-demo-rpi-1",
# "endpoint": "a1bqyju1450wf9-ats.iot.eu-west-1.amazonaws.com",
# "port": 8883,
# "security":[
#     {"root": "./certs/root-ca.pem"},
#     {"cert": "./certs/8098cdfe96-certificate.pem.crt"},
#     {"private": "./certs/8098cdfe96-private.pem.key"}
# ],
# "mode": "STAND"

class ProviderConfig:
    def __init__(self, config):
        # check if an object or not
        if isinstance(config, dict) == False:
            raise TypeError()

        try:
            self.__name = config["type"]
            self.__clientId = config["client_id"]
            self.__thingId = config["thing_id"]
            self.__endpoint = config["endpoint"]
            self.__port = config["port"]
            self.__security = []
            for key in config["security"]:
                self.__security.append(key)
            self.__mode = config["mode"]

            if self.__endpoint == "" or self.__thingId == "":
                raise ValueError()
        except KeyError:
            raise ValueError()

    @property    
    def Name(self):
        return self.__name

    @property    
    def ClientId(self):
        return self.__clientId

    @ClientId.setter
    def ClientId(self, clientId):
        self.__clientId = clientId

    @property    
    def ThingId(self):
        return self.__thingId

    @property    
    def Endpoint(self):
        return self.__endpoint        

    @property    
    def Port(self):
        return self.__port 

    @property    
    def Security(self):
        return self.__security

    def get_security_key(self, key):
        for security in self.__security:
            if key in security.keys():
                return security
        return None

    @property    
    def Mode(self):
        return self.__mode           