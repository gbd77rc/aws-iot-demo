import unittest
import logging
import time
import sys

import platform
if platform.machine() == 'x86_64':
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi     # Fake RPi (GPIO)
    fake_rpi.toggle_print(False)

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.control.lights import Lights

class Subscriber():
    def __init__(self, test):
        self.testing = test

    def update(self, event, message):
        self.testing.assertTrue(event, "sensor")
        logging.debug("Dispatched event [{}] with message [{}]".format(event, message))

class Lights_Tests(unittest.TestCase):
    config = {}
    def setUp(self):
        self.config = {
            "aws": {
                "telemetry_topic": "telemetry/rpi-1",
                "control_topic": "control/rpi-1",
                "client_id": "rpi-1",
                "thing_id": "iot-demo-rpi-1",
                "endpoint": "a1bqyju1450wf9-ats.iot.eu-west-1.amazonaws.com",
                "port": 8883,
                "root": "./certs/root-ca.pem",
                "cert": "./certs/8098cdfe96-certificate.pem.crt",
                "private": "./certs/8098cdfe96-private.pem.key"
            },
            "sensor": {
                "temp_pin": 4,
                "polling": 5
            },
            "leds": {
                "blink": 500,
                "colours": [{
                    "colour": "Green",
                    "pin": 26
                }, {
                    "colour": "Yellow",
                    "pin": 19
                }, {
                    "colour": "Red",
                    "pin": 13
                }]
            }
        }

    def test_get_state(self):
        lights = Lights(self.config)
        state = lights.get_state()
        self.assertEqual(len(state.keys()), 3)

    def test_subscribe(self):
        lights = Lights(self.config)
        lights.subscribe()
        state = lights.get_state()
        lights.unsubscribe()
        self.assertEqual(len(state.keys()), 3)

    def test_publish(self):
        lights = Lights(self.config)
        lights.register(Subscriber(self))
        leds = {
            "green": "on"
        }
        lights.toogle(leds)
        time.sleep(1)
        self.assertEqual(lights.get_dispatch_count(), 1)
        leds = {
            "green": "on"
        }
        lights.toogle(leds)
        time.sleep(1)
        self.assertEqual(lights.get_dispatch_count(), 1)
        leds = {
            "green": "on",
            "yellow": "blink"
        }
        lights.toogle(leds)
        time.sleep(1)
        self.assertEqual(lights.get_dispatch_count(), 2)
        leds = {
            "green": "off",
            "yellow": "off"
        }
        lights.toogle(leds)
        self.assertEqual(lights.get_dispatch_count(), 3)
        
    def test_singleton(self):
        a = Lights(self.config)
        b = Lights(self.config)

        leds = {
            "green": "on"
        }
        a.toogle(leds)

        astate = a.get_state()
        bstate = b.get_state()

        self.assertEqual(astate, bstate)



if __name__ == '__main__':
    unittest.main()