import logging
import time
import json
from threading import Thread, Event
from demo.provider.aws import AwsProvider
from demo.devices.led import Led

logger = logging.getLogger(__name__)

class Lights:
    __client = {}
    __lights = []
    __event = {}

    def __init__(self, config):
        self.__config = config
        self.__event = Event()
        provider = AwsProvider(self.__config)
        self.__client = provider.get_client()

        for led in config["leds"]["colours"]:
            self.__lights.append(Led(led["colour"], led["pin"]))

        self.__event = Event()
        logger.debug("Initialised {} lights".format(len(self.__lights)))

    def __callback(self, client, userdata, message):
        msg = json.loads(message.payload.decode('utf-8'))
        logger.debug("Payload is {}".format(msg))

        for key in msg:
            # Check if in leds
            logger.debug("Processing item in msg[{}]".format(key))
            for light in self.__lights:
                if light.get_name().lower() == key.lower():
                    led_off = msg[key].lower() == "off"
                    if led_off:
                        if light.is_blinking():
                            light.blink_off()
                        else: 
                            light.off()
                    else: 
                        if msg[key].lower() in ('blink', 'blinking') and light.is_blinking() == False:
                            light.blink_on(self.__config["leds"]["blink"])
                        elif light.is_on() == False: 
                            light.on()


    def subscribe(self):
        self.__client.subscribeAsync(self.__config["aws"]["control_topic"], 1, messageCallback=self.__callback)

    def unsubscribe(self):
        self.__client.unsubscribeAsync(self.__config["aws"]["control_topic"])

    def get_state(self):
        state = {}
        for light in self.__lights:
            state.update(light.get_state())
        
        return state
    
    
    