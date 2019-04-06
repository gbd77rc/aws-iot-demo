import unittest
import logging

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")
import sys
import platform
if platform.machine() == 'x86_64':
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi     # Fake RPi (GPIO)
    fake_rpi.toggle_print(False)

from demo.devices.dht11 import DHT11

class DHT11_Tests(unittest.TestCase):
    dht11 = {}
    def setUp(self):
        self.dht11 = DHT11(pin=2)

    def test_reading(self):
        value = self.dht11.read()
        self.assertTrue(value.error_code > 0)
        self.assertTrue(value.temperature == 0)
        self.assertTrue(value.humidity == 0)

if __name__ == '__main__':
    unittest.main()