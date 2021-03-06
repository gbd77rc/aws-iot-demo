import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from AWSIoTPythonSDK.exception import AWSIoTExceptions
from demo.common.singleton import Singleton

logger = logging.getLogger(__name__)

class AwsProvider(metaclass=Singleton):
    __config = {}
    __client = None
    __shadow = None
    __shadowHandle= None
    __instance = None

    def __init__(self, config):
        self.__config = config
        logger.debug("Initialising AWS Provider...")
        self.__init_shadow()
    
    def __init_client(self):
        self.__client = AWSIoTMQTTClient(self.__config["aws"]["client_id"])
        try:
            self.__client.configureEndpoint(self.__config["aws"]["endpoint"], self.__config["aws"]["port"])
            logger.info("Trying to connect to {}:{}".format(self.__config["aws"]["endpoint"],self.__config["aws"]["port"]))
            self.__client.configureCredentials(self.__config["aws"]["root"],
                                            self.__config["aws"]["private"],
                                            self.__config["aws"]["cert"])

            # Infinite offline Publish queueing
            self.__client.configureOfflinePublishQueueing(-1)
            self.__client.configureDrainingFrequency(2)  # Draining: 2 Hz
            self.__client.configureConnectDisconnectTimeout(10)  # 10 sec
            self.__client.configureMQTTOperationTimeout(5)  # 5 sec

            self.__client.connect()
        except AWSIoTExceptions.connectTimeoutException as error:
            logger.error("Problem with MQTT configuration: {}".format(error))  
        logger.debug("Initialised AWS Standard Client...")

    def __init_shadow(self):
        self.__shadow = AWSIoTMQTTShadowClient(self.__config["aws"]["client_id"] + "_shadow")
        try:
            self.__shadow.configureEndpoint(self.__config["aws"]["endpoint"], self.__config["aws"]["port"])
            logger.info("Trying to connect to {}:{}".format(self.__config["aws"]["endpoint"],self.__config["aws"]["port"]))
            self.__shadow.configureCredentials(self.__config["aws"]["root"],
                                            self.__config["aws"]["private"],
                                            self.__config["aws"]["cert"])

            # Infinite offline Publish queueing
            self.__shadow.configureAutoReconnectBackoffTime(1, 32, 20)
            self.__shadow.configureConnectDisconnectTimeout(10)  # 10 sec
            self.__shadow.configureMQTTOperationTimeout(5)  # 5 sec

            self.__shadow.connect()
            self.__shadowHandle = self.__shadow.createShadowHandlerWithName(self.__config["aws"]["thing_id"], True)
        except AWSIoTExceptions.connectTimeoutException as error:
            logger.error("Problem with MQTT configuration: {}".format(error))  
        logger.debug("Initialised AWS Standard Client...")

    def get_client(self):
        if self.__client is None:
            self.__init_client()
        return self.__client

    def get_shadow_handle(self):
        if self.__shadowHandle is None:
            self.__init_shadow()
            
        return self.__shadowHandle        