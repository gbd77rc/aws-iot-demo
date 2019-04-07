import logging
import time
import json
from threading import Thread, Event
from demo.provider.aws import AwsProvider
from demo.devices.led import Led
from demo.common.publisher import Publisher
from demo.common.singleton import Singleton

logger = logging.getLogger(__name__)

class Lights(Publisher, metaclass=Singleton):
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
        super().__init__(["lights"])
        logger.debug("Initialised {} lights".format(len(self.__lights)))

    def __callback(self, client, userdata, message):
        msg = json.loads(message.payload.decode('utf-8'))
        logger.debug("Payload is {}".format(msg))
        self.toogle(msg)

    def __should_change_state(self, current, new_state):
        #Check if current blinking and we want to be blinking, there we don't want to change state
        if current == 'blinking' and new_state in ('blink', 'blinking'):
            return False

        #Check if current is on/off and new state is on/off, if so then don't want to change if same
        if current == new_state:
            return False
        return True

    def toogle(self, msg):
        state = {}
        for key in msg:
            # Check if in leds
            logger.debug("Processing item in msg[{}]".format(key))
            
            # Process the current lights and see if we are known
            for light in self.__lights:
                if light.get_name().lower() == key.lower():
                    current = list(light.get_state().values())[0]
                    if self.__should_change_state(current, msg[key].lower()):
                        logger.debug('The current state [{}] is different to new state [{}]'.format(current, msg[key].lower()))
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
        state = self.get_state()
        if len(state.keys()) > 0:     
            self.dispatch("lights", state)           
                    
    def subscribe(self):
        self.__client.subscribeAsync(self.__config["aws"]["control_topic"], 1, messageCallback=self.__callback)

    def unsubscribe(self):
        self.__client.unsubscribeAsync(self.__config["aws"]["control_topic"])

    def get_state(self):
        state = {}
        for light in self.__lights:
            state.update(light.get_state())
        
        return state
    
    def register(self, who, callback=None):
        super().register("lights", who, callback)

    def unregister(self, who):
        super().unregister("lights", who)
    