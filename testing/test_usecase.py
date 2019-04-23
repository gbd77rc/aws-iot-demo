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

from demo.usecases.usecase import UseCase
from demo.config.usecaseconfig import UseCaseConfig
from demo.devices.deviceloader import DeviceLoader
from demo.devices.devicetype import DeviceType

class UseCase_Tests(unittest.TestCase):
    def test_type_exception(self):
        self.assertRaises(TypeError, UseCase, None)

    def test_config_info(self):
        a = UseCaseConfig({
            "use-case": "Test-1",
            "push": 0,
            "payload-type": "JSON",
            "devices": ["DHT-11"]
        })

        b = UseCase(a)

        self.assertEqual(len(b.Devices), 0)
        self.assertEqual(b.Config.Name, a.Name)

    def test_load_devices(self):
        a = UseCaseConfig({
            "use-case": "Test-1",
            "push": 0,
            "payload-type": "JSON",
            "devices": ["Sensor"]
        })

        b = UseCase(a)

        loader = DeviceLoader()
        loader.load_devices([{
            "name": "Sensor",
            "type": "dht11",
            "pin": 6
        }])

        self.assertRaises(ValueError, b.load_devices, None)
        self.assertRaises(ValueError, b.load_devices, [{"Name":"Dummy"}])

        b.load_devices(loader.Devices)

        self.assertEqual(len(b.Devices), len(b.Config.DeviceNames))
        self.assertEqual(b.Devices[0].Config.Type, DeviceType.DHT11)
   

   
if __name__ == '__main__':
    unittest.main()        