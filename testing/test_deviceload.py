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
        self.assertEqual(loader.Devices[0].Config.Name, "Sensor")
        self.assertEqual(loader.Devices[0].Config.Friendly, "Sensor (DHT-11)")

    def test_load_led(self):
        loader = DeviceLoader()
        loader.load_devices([{
            "name": "Green",
            "type": "led",
            "pin": 6
        }])

        self.assertEqual(len(loader.Devices), 1)
        self.assertEqual(loader.Devices[0].Config.Type, DeviceType.LED)
        self.assertEqual(loader.Devices[0].Config.Friendly, "Green (LED)")

    def test_load_cpup(self):
        loader = DeviceLoader()
        loader.load_devices([{
            "name": "CPU Info",
            "type": "cpuperc"
        }])

        self.assertEqual(len(loader.Devices), 1)
        self.assertEqual(loader.Devices[0].Config.Type, DeviceType.CPUPERCENT)
        self.assertEqual(loader.Devices[0].Config.Friendly, "CPU Info (CPU Percentage Used)")

    def test_load_cput(self):
        loader = DeviceLoader()
        loader.load_devices([{
            "name": "CPU Info",
            "type": "cputemp"
        }])

        self.assertEqual(len(loader.Devices), 1)
        self.assertEqual(loader.Devices[0].Config.Type, DeviceType.CPUTEMP)
        self.assertEqual(loader.Devices[0].Config.Friendly, "CPU Info (CPU Temperature)")

    def test_load_mem(self):
        loader = DeviceLoader()
        loader.load_devices([{
            "name": "Memory Info",
            "type": "memory"
        }])

        self.assertEqual(len(loader.Devices), 1)
        self.assertEqual(loader.Devices[0].Config.Type, DeviceType.MEMORY)
        self.assertEqual(loader.Devices[0].Config.Friendly, "Memory Info (Memory Information in Bytes)")

    def test_load_multiple(self):
        loader = DeviceLoader()
        loader.load_devices([{
            "name": "Memory Info",
            "type": "memory"
        },{
            "name": "Green",
            "type": "led",
            "pin": 26
        },{
            "name": "Yellow",
            "type": "led",
            "pin": 27
        },{
            "name": "Red",
            "type": "led",
            "pin": 28
        }])

        self.assertEqual(len(loader.Devices), 4)
        self.assertEqual(loader.Devices[0].Config.Type, DeviceType.MEMORY)
        self.assertEqual(loader.Devices[0].Config.Friendly, "Memory Info (Memory Information in Bytes)")
        self.assertEqual(loader.Devices[1].Config.Type, DeviceType.LED)

if __name__ == '__main__':
    unittest.main()