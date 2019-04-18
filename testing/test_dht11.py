import unittest
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")
import sys
import platform
if platform.machine() == 'x86_64':
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi     # Fake RPi (GPIO)
    fake_rpi.toggle_print(False)

from demo.config.deviceconfig import DeviceConfig
from demo.devices.dht11 import DHT11

class DHT11_Tests(unittest.TestCase):
    dht11 = {}
    config = None
    def setUp(self):
        self.config = DeviceConfig({
            "name": "Sensor",
            "type": "dht11",
            "pin": 6
        })
        self.dht11 = DHT11(self.config)

    def test_reading(self):
        value = self.dht11.read()
        self.assertFalse(value.IsValid)
        logging.info("Reading is [{}]".format(value.to_json(pretty=True)))

if __name__ == '__main__':
    unittest.main()