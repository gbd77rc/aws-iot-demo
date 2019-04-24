import time
import RPi.GPIO as GPIO
import logging
import platform
from enum import Enum
from threading import Thread, Event

logger = logging.getLogger(__name__)

from demo.config.deviceconfig import DeviceConfig
from demo.devices.deviceresult import DeviceResult
from demo.devices.devicebase import DeviceBase
from demo.devices.devicetype import DeviceType
from demo.devices.directiontype import DirectionType

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

class State(Enum):
    off = 0,
    on = 1
    
class Led(DeviceBase):
    __state = State.off
    __event = {}
    __blinking = False

    def __init__(self, config):
        super().__init__(config, DeviceType.LED, DirectionType.OUT)
        GPIO.setup(super().Config.Pin, GPIO.OUT)
        logger.debug("Initialised LED ({}) on PIN {}".format(
            super().Config.Name, super().Config.Pin))
        self.__event = Event()

    def __blink(self, blink_delay):
        logger.debug("{} Led blinking is enabled for {}ms".format(super().Config.Name, blink_delay))
        self.__blinking = True
        while not self.__event.is_set():
            self.on()
            self.__event.wait(blink_delay/1000.0) # It only accepts seconds so divide by 1000.0 and get ms.  The .0 is important or you get 0!
            self.off()
            self.__event.wait(blink_delay/1000.0) # It only accepts seconds so divide by 1000.0 and get ms.  The .0 is important or you get 0!
        self.__blinking = False
        logger.debug("{} Led blinking is disabled".format(super().Config.Name))


    def on(self):   
        GPIO.output(super().Config.Pin, GPIO.HIGH)
        self.__state = State.on
        logger.debug("{} Led is on".format(super().Config.Name))

    def off(self):
        GPIO.output(super().Config.Pin, GPIO.LOW)
        self.__state = State.off
        logger.debug("{} Led is off".format(super().Config.Name))

    def blink_on(self, blink_delay):
        logger.debug("{} Led is blink {} is on {}".format(super().Config.Name, 
            "Yes" if self.is_blinking() else "No",
            "Yes" if self.is_on() else "No"))
        if self.is_blinking():
            self.blink_off()
        if self.is_on():
            self.off()

        self.thread = Thread(target=self.__blink, args=[blink_delay])
        self.thread.start()

    def blink_off(self):
        self.__event.set()
        self.thread.join()   

    def get_state(self):
        state ={}
        #The name has a post fix of (LED) so lets get rid of that
        name = super().Config.Name.replace(" (LED)", "").lower()
        state[name] = 'blinking' if self.__blinking else self.__state.name.lower()
        return state

    def is_blinking(self):
        return self.__blinking

    def is_on(self):
        return self.__state == State.on

    def get_name(self):
        return super().Config.Name
    
    def write(self, value):
        if value > 0:
            self.on()
        else:
            self.off()