import json
import time
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

from threading import Thread, Event
from demo.config.usecaseconfig import UseCaseConfig
from demo.devices.devicebase import DeviceBase
from demo.common.publisher import Publisher
from demo.devices.directiontype import DirectionType

class UseCase(Publisher):
    __thread ={}
    def __init__(self, config):
        if isinstance(config, UseCaseConfig) == False:
            raise TypeError()
        self.__config = config
        self.__devices = []
        self.__event = Event()
        self.__started = False
        super().__init__(["use-case"])

    @property
    def Config(self):
        return self.__config

    @property
    def Devices(self):
        return self.__devices

    def __reading(self):
        logger.debug("Starting to read temperature every {} second(s)".format(self.Config.Wait))
        while not self.__event.is_set():
            body = self.get_reading()
            msg = json.dumps(body)
            logger.debug("Publishing Message at {}: [{}]".format(time.time(), msg))
            self.dispatch("use-case", body)
            self.__event.wait(self.Config.Wait)     

    def get_reading(self):
        body = {
            "results":[]
        }
        isValid = True
        for device in self.__devices:
            if device.Direction == DirectionType.IN:
                result = device.read()
                if isValid == True and result.IsValid == False:
                    isValid = False
                body["results"].append(result.to_json())

        body["epoch"] = datetime.utcnow().strftime('%Y%m%d %H:%M:%S.%f')
        body["valid"] = isValid
        return body               

    def load_devices(self, devices):
        if isinstance(devices, list) == False:
            raise ValueError()
        
        for device in devices:
            logger.debug("Device being checked is [{}]".format(device))
            if isinstance(device, DeviceBase) == False:
                raise ValueError()

            for name in self.__config.DeviceNames:
                logger.debug("Device Name is [{}]".format(name))
                if name == device.Config.Name:
                    self.__devices.append(device)

    def start(self):
        logger.debug("Starting {} use case.".format(self.Config.Name))
        self.__started = True
        self.__thread = Thread(target=self.__reading)
        self.__thread.start()     

    def stop(self):
        logger.debug("Stopping {} use case.".format(self.Config.Name))
        self.__started = False
        self.__event.set()
        self.__thread.join()
     
    def register(self, who, callback=None):
        super().register("use-case", who, callback)

    def unregister(self, who):
        super().unregister("use-case", who)


        