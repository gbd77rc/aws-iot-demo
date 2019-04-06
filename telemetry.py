from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from AWSIoTPythonSDK.exception import AWSIoTExceptions

import os
import json
import RPi.GPIO as GPIO
import dht11
import logging
import time
from enum import Enum
import threading

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logFormatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
rootLogger = logging.getLogger("telemetry-app")

with open('./config.json') as config_file:
    config = json.load(config_file)

fileHandler = logging.FileHandler(config["logging"]["location"])
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.ERROR)
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# level = getattr(logging, config["logging"]["level"].upper())
# print("Going to set the logging level to {}({})".format(level , config["logging"]["level"].upper()))
# consoleHandler.setLevel(level)
rootLogger.addHandler(fileHandler)
# rootLogger.addHandler(consoleHandler)


class Action(Enum):
    off = 0,
    on = 1,
    blink = 2


state = {}
state["leds"] = {"red": "off", "yellow": "off", "green": "off"}


def read_temp():
    # read data using pin 14
    instance = dht11.DHT11(pin=config["sensor"]["temp_pin"])
    result = instance.read()
    rootLogger.debug("Temperature is {}c and Humidity is {}%".format(
        result.temperature, result.humidity))
    return result


def toggle_led(key, toggle):
    global state
    shadow = {}
    shadow["state"] = {}
    for led in config["leds"]["colours"]:
        rootLogger.debug("Processing led [{}]".format(led["colour"]))
        if (led["colour"].lower() == key.lower()):
            action = Action[toggle].value[0]
            rootLogger.debug("Setting [{}] led to [{}:{}] on pin [{}]".format(
                key, toggle, action, led["pin"]))
            GPIO.setup(led["pin"], GPIO.OUT)
            GPIO.output(led["pin"], action)
            state["leds"][key.lower()] = toggle
    shadow["state"]["desired"] = state
    rootLogger.debug("Shadow Publishing [{}]".format(json.dumps(shadow)))


def controlCallback(client, userdata, message):
    msg = json.loads(message.payload.decode('utf-8'))
    rootLogger.info("Payload is {}".format(msg))

    for key in msg:
        # Check if in leds
        rootLogger.debug("Processing item in msg[{}]".format(key))
        toggle_led(key, msg[key].lower())


def initialise_client():
    myMQTTClient = AWSIoTMQTTClient(config["aws"]["client_id"])
    try:
        myMQTTClient.configureEndpoint(config["aws"]["endpoint"], 8883)
        rootLogger.info("Trying to connect to {}".format(
            config["aws"]["endpoint"]))
        myMQTTClient.configureCredentials(config["aws"]["root"],
                                          config["aws"]["private"],
                                          config["aws"]["cert"])

        # Infinite offline Publish queueing
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        myMQTTClient.connect()
    except AWSIoTExceptions.connectTimeoutException as error:
        rootLogger.error("Problem with MQTT configuration: {}".format(error))
    return myMQTTClient


def initialise_shadow_client():
    myMQTTShadowClient = AWSIoTMQTTShadowClient(config["aws"]["shadow_id"])
    try:
        myMQTTShadowClient.configureEndpoint(config["aws"]["endpoint"], 8883)
        rootLogger.info("Trying to shadow connect to {}".format(
            config["aws"]["endpoint"]))
        myMQTTShadowClient.configureCredentials(config["aws"]["root"],
                                                config["aws"]["private"],
                                                config["aws"]["cert"])

        # Infinite offline Publish queueing
        myMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

        myMQTTShadowClient.connect()
    except AWSIoTExceptions.connectTimeoutException as error:
        rootLogger.error(
            "Problem with Shadow MQTT configuration: {}".format(error))

    return myMQTTShadowClient


def publish_reading(reading, client):
    if reading.temperature == 0 and reading.humidity == 0:
        rootLogger.warn(
            "As both are 0 then we assume that the reading failed so not sending message")
        return
    body = {}
    body['temperature'] = reading.temperature
    body["humidity"] = reading.humidity
    body["device_id"] = config["aws"]["client_id"]
    body["epoch"] = time.time()
    msg = json.dumps(body)
    rootLogger.debug("Publishing Message: {}".format(msg))
    client.publish(config["aws"]["telemetry_topic"], msg, 1)


# Shadow JSON schema:
#
# Name: Bot
# {
#	"state": {
#		"desired":{
#			"property":<INT VALUE>
#		}
#	}
# }

# Custom Shadow callback
def customShadowUpdate(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~ SHADOW ~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("property: " + str(payloadDict["state"]["desired"]["property"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")


def customShadowDelete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


def looper():
    myMQTTClient = initialise_client()
    myMQTTShadowClient = initialise_shadow_client()

    if myMQTTClient is None or myMQTTShadowClient is None:
        return
    myMQTTClient.subscribeAsync(
        config["aws"]["control_topic"], 1, messageCallback=controlCallback)

    while True:
        rootLogger.info("Waiting to Poll...")
        time.sleep(config["sensor"]["polling"])
        rootLogger.debug("Reading Temperature....")
        reading = read_temp()
        publish_reading(reading, myMQTTClient)


if __name__ == '__main__':
    size = len(config["leds"]["colours"])
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    looper()


def function_handler(event, context):
    return
