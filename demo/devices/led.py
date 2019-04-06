import time
import RPi.GPIO as GPIO
import logging
import platform
from enum import Enum
from threading import Thread, Event

logger = logging.getLogger(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

class State(Enum):
    off = 0,
    on = 1
    
class Led:
    __name = ""
    __state = State.off
    __pin = 0
    __event = {}
    __blinking = False

    def __init__(self, name, pin):
        self.__pin = pin
        self.__name = name
        GPIO.setup(self.__pin, GPIO.OUT)
        logger.debug("Initialised LED ({}) on PIN {}".format(
            self.__name, self.__pin))
        self.__event = Event()

    def __blink(self, blink_delay):
        logger.debug("{} Led blinking is enabled for {}ms".format(self.__name, blink_delay))
        self.__blinking = True
        while not self.__event.is_set():
            self.on()
            self.__event.wait(blink_delay/1000.0) # It only accepts seconds so divide by 1000.0 and get ms.  The .0 is important or you get 0!
            self.off()
            self.__event.wait(blink_delay/1000.0) # It only accepts seconds so divide by 1000.0 and get ms.  The .0 is important or you get 0!
        self.__blinking = False
        logger.debug("{} Led blinking is disabled".format(self.__name))


    def on(self):   
        GPIO.output(self.__pin, GPIO.HIGH)
        self.__state = State.on
        logger.debug("{} Led is on".format(self.__name))

    def off(self):
        GPIO.output(self.__pin, GPIO.LOW)
        self.__state = State.off
        logger.debug("{} Led is off".format(self.__name))

    def blink_on(self, blink_delay):
        logger.debug("{} Led is blink {} is on {}".format(self.__name, 
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
        state[self.__name.lower()] = self.__state.name.lower()
        return state

    def is_blinking(self):
        return self.__blinking

    def is_on(self):
        return self.__state == State.on

    def get_name(self):
        return self.__name