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

class Lights_Tests(unittest.TestCase):
    config = {}
    def setUp(self):
        self.config = {
            "aws": {
                "telemetry_topic": "telemetry/rpi-1",
                "control_topic": "control/rpi-1",
                "client_id": "rpi-1",
                "shadow_id": "iot-demo-rpi-1",
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

        

if __name__ == '__main__':
    unittest.main()