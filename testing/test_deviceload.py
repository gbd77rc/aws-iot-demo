import unittest
import logging
import time
import sys
import json

import platform
if platform.machine() == 'x86_64':
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi     # Fake RPi (GPIO)
    fake_rpi.toggle_print(False)

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.config.deviceconfig import DeviceConfig
from demo.devices.deviceloader import DeviceLoader
from demo.devices.devicetype import DeviceType

class DeviceLoader_Tests(unittest.TestCase):
    def test_load_dht11(self):
        loader = DeviceLoader()
        loader.load_devices([{
            "name": "Sensor",
            "type": "dht11",
            "pin": 6
        }])

        self.assertEqual(len(loader.Devices), 1)
        self.assertEqual(loader.Devices[0].Config.Type, DeviceType.DHT11)



if __name__ == '__main__':
    unittest.main()