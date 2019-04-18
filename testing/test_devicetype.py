import unittest
import logging
import time
import sys
import json

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.devices.devicetype import DeviceType

class DeviceType_Tests(unittest.TestCase):
    def test_are_equal(self):
        a = DeviceType.DHT11
        b = DeviceType.DHT11
        self.assertEqual(a, b)

    def test_are_not_equal(self):
        a = DeviceType.DHT11
        b = DeviceType.CPUPRECENT
        self.assertNotEqual(a, b)
       
    def test_string_to_type(self):
        expected = DeviceType.DHT11
        b = DeviceType.get_type("dht11")
        self.assertEqual(expected, b)       

    def test_get_friendly(self):
        expected = "CPU Temperature"
        a = DeviceType.CPUTEMP
        self.assertEqual(expected, a.get_friendly())          