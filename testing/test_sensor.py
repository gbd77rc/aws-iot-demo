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

from demo.telemetry.sensor import Sensor

class Sensor_Tests(unittest.TestCase):
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
            }
        }

    def test_start_stop(self):
        sensor =  Sensor(self.config)
        sensor.start()
        time.sleep(2)
        current = time.process_time()
        sensor.stop()
        elapsed = time.process_time()
        logging.debug("Elapsed is {}".format((elapsed - current)))
        self.assertTrue((elapsed - current) < 1.0)


        

if __name__ == '__main__':
    unittest.main()