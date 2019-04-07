import logging
import json
from threading import Thread, Event

logger = logging.getLogger(__name__)

from demo.provider.aws import AwsProvider
from demo.control.lights import Lights

class Service:
    __shadow = {}
    __state = {}
    __lights = {}

    def __init__(self, config):
        self.__config = config
        self.__event = Event()
        provider = AwsProvider(self.__config)
        self.__shadow = provider.get_shadow_handle()
        self.__lights = Lights(self.__config)
        self.__lights.register(self, self.update)
        logger.debug("Shadow Handle is {}".format(self.__shadow) )       

    # {"version":5,"timestamp":1554580866,"state":{"green":"off"},"metadata":{"green":{"timestamp":1554580866}}}
    def __delta_callback(self,payload, responseStatus, token):
        logger.debug("Delta Callback payload is {}".format(payload))
        current = json.loads(payload)
        # Process the desired state first to see if we can set the LEDs to the correct state
        for key in current["state"]:
            logger.debug("Delta state item is {}".format(key))
            # Check if led or not
            if key == 'lights':
                self.__lights.toogle(current["state"][key]) 

    def __updated_callback(self, payload, responseStatus, token):
        logger.debug("Updated Callback payload is {}".format(payload))

    # {"state":{"desired":{"welcome":"aws-iot",
    # "lights":{"green":"on","yellow":"off","red":"off"}},
    # "reported":{"welcome":"aws-iot"},
    # "delta":{"lights":{"green":"on","yellow":"off","red":"off"}}},
    # "metadata":{"desired":{"welcome":{"timestamp":1554635548},
    # "lights":{"green":{"timestamp":1554635548},"yellow":{"timestamp":1554635548},"red":{"timestamp":1554635548}}},
    # "reported":{"welcome":{"timestamp":1554635548}}},
    # "version":15,"timestamp":1554635569,"clientToken":"4c826256-a9ee-4270-ada8-b9104c8ea7fb"}
    def __get_callback(self, payload, responseStatus, token):
        logger.debug("Get Callback status is {} payload is {}".format(responseStatus, payload))
        current = json.loads(payload)
        # Process the desired state first to see if we can set the LEDs to the correct state
        for key in current["state"]["desired"]:
            logger.debug("Desired state item is {}".format(key))
            # Check if led or not
            if key == 'lights':
                self.__lights.toogle(current["state"]["desired"][key])    

    def start(self):
        self.__shadow.shadowRegisterDeltaCallback(self.__delta_callback)    
        self.__shadow.shadowGet(self.__get_callback, 30)    

    def stop(self):
        self.__shadow.shadowUnregisterDeltaCallback()

    def update(self, event, message):
        logger.debug("Event [{}] was published with [{}] message".format(event,message))

        if event == "sensors":
            message = {
                "temperature": message["temperature"],
                "humidity": message["humidity"],
                "cpu_temp": message["cpu_temp"]
            }
        
        reported = {
            "state":{
                "reported":{
                    event: message
                }
            }
        }
        j = json.dumps(reported)
        logger.debug("Publishing to Shadow [{}]".format(j))
        self.__shadow.shadowUpdate(j, self.__updated_callback, 30)
