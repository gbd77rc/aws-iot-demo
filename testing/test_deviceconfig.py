import unittest
import logging
import time
import sys
import json

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.config.deviceconfig import DeviceConfig
from demo.devices.devicetype import DeviceType

class DeviceConfig_Tests(unittest.TestCase):
    def test_type_exception(self):
        self.assertRaises(TypeError, DeviceConfig, None)

    def test_value_exception(self):
        self.assertRaises(ValueError, DeviceConfig, {})
        self.assertRaises(ValueError, DeviceConfig, {
            "name": "Test-1"
        })
        self.assertRaises(ValueError, DeviceConfig, {
            "name": ""
        })
        self.assertRaises(ValueError, DeviceConfig, {
            "name": "Test-1",
            "type": ""
        })

        self.assertRaises(ValueError, DeviceConfig, {
            "name": "Test-1",
            "type": "test"
        })

    def test_pin_config(self):
        a = DeviceConfig({
            "name": "Sensor",
            "type": "dht11",
            "pin": 6
        })

        self.assertEqual(a.Type, DeviceType.DHT11)
        self.assertEqual(a.Pin, 6)
        self.assertEqual(a.Name, "Sensor (DHT-11)")