import logging
import time
import json
from threading import Thread, Event
from demo.provider.aws import AwsProvider
from demo.devices.dht11 import DHT11
from demo.common.publisher import Publisher

logger = logging.getLogger(__name__)

class Sensor(Publisher):
    __sensor = {}
    __config = {}
    __event = {}
    __thread ={}

    def __init__(self, config):
        self.__sensor = DHT11(config["sensor"]["temp_pin"])
        self.__config = config
        self.__event = Event()
        provider = AwsProvider(self.__config)
        self.__client = provider.get_client()
        super().__init__(["sensor"])
        logger.debug("Initialised Temperature Sensor on pin {} with polling of {} second(s)".format(self.__config["sensor"]["temp_pin"], self.__config["sensor"]["polling"]))

    def __reading(self):
        logger.debug("Starting to read temperature every {} second(s)".format(self.__config["sensor"]["polling"]))
        while not self.__event.is_set():
            body = self.get_reading()
            msg = json.dumps(body)
            logger.debug("Publishing Message: {}".format(msg))
            self.__client.publish(self.__config["aws"]["telemetry_topic"], msg, 1)
            self.dispatch("sensor", msg)
            self.__event.wait(self.__config["sensor"]["polling"])


    def start(self):
        logger.debug("Starting reading sensor in a loop...")
        self.__started = True
        self.__thread = Thread(target=self.__reading)
        self.__thread.start()        

    def stop(self):
        logger.debug("Stopping reading sensor in a loop...")
        self.__started = False
        self.__event.set()
        self.__thread.join()

    def get_reading(self):
        result = self.__sensor.read()
        body = {}
        body['temperature'] = result.temperature
        body["humidity"] = result.humidity
        body["device_id"] = self.__config["aws"]["client_id"]
        body["epoch"] = time.time()
        body["valid"] = True if result.temperature != 0 and result.humidity != 0 else False
        logger.debug("Reading: Temperature is [{}]c Humidity is [{}]%".format(result.temperature, result.humidity))
        return body

    def register(self, who, callback=None):
        super().register("sensor", who, callback)

    def unregister(self, who):
        super().unregister("sensor", who)