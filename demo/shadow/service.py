import logging
import json
from threading import Thread, Event

logger = logging.getLogger(__name__)

from demo.provider.aws import AwsProvider

class Service:
    __shadow = {}
    __state = {}

    def __init__(self, config):
        self.__config = config
        self.__event = Event()
        provider = AwsProvider(self.__config)
        self.__shadow = provider.get_shadow_handle()
        logger.debug("Shadow Handle is {}".format(self.__shadow) )       

    # {"version":5,"timestamp":1554580866,"state":{"green":"off"},"metadata":{"green":{"timestamp":1554580866}}}
    def __delta_callback(self,payload, responseStatus, token):
        logger.debug("Delta Callback payload is {}".format(payload))

    def __updated_callback(self, payload, responseStatus, token):
        logger.debug("Updated Callback payload is {}".format(payload))

    # {"state":{"desired":{"welcome":"aws-iot","green":"off"},
    # "reported":{"welcome":"aws-iot"},
    # "delta":{"green":"off"}},
    # "metadata":{"desired":{"welcome":{"timestamp":1554580866},
    # "green":{"timestamp":1554580866}},
    # "reported":{"welcome":{"timestamp":1554580866}}},
    # "version":5,"timestamp":1554581409,"clientToken":"441e3597-9820-4e3c-8eeb-08c6323e48ce"} 
    def __get_callback(self, payload, responseStatus, token):
        logger.debug("Get Callback status is {} payload is {}".format(responseStatus, payload))
        current = json.loads(payload)
        # Process the desired state first to see if we can set the LEDs to the correct state
        for key in current["state"]["desired"]:
            logger.debug("Desired state item is {}".format(item))
            # Check if led or not
            if key == 'lights':
                for light in current["state"]["desired"][key]:
                    
                    

        
    def start(self):
        self.__shadow.shadowRegisterDeltaCallback(self.__delta_callback)    
        self.__shadow.shadowGet(self.__get_callback, 30)    

    def stop(self):
        self.__shadow.shadowUnregisterDeltaCallback()

    def update(self, event, message):
        logger.debug("Event [{}] was published with [{}] message".format(event,message))
        reported = {
            "state":{
                "reported":{
                    "green":"on"
                }
            }
        }
        self.__shadow.shadowUpdate(json.dumps(reported), self.__updated_callback, 30)
