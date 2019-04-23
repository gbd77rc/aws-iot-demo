import unittest
import logging
import time
import sys
import json

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.config.usecaseconfig import UseCaseConfig

class UseCaseConfig_Tests(unittest.TestCase):
    def test_type_exception(self):
        self.assertRaises(TypeError, UseCaseConfig, None)

    def test_value_exception(self):
        self.assertRaises(ValueError, UseCaseConfig, {})
        self.assertRaises(ValueError, UseCaseConfig, {
            "use-case": ""
        })
        self.assertRaises(ValueError, UseCaseConfig, {
            "use-case": "Test-1",
            "push": 0,
            "payload-type": "",
            "devices": []
        })
        self.assertRaises(ValueError, UseCaseConfig, {
            "use-case": "Test-1",
            "push": 0,
            "payload-type": "BYTES",
            "devices": []
        })

        self.assertRaises(ValueError, UseCaseConfig, {
            "use-case": "Test-1",
            "push": 0,
            "payload-type": "JSON",
            "devices": []
        })

    def test_wait_is_1(self):
        a = UseCaseConfig({
            "use-case": "Test-1",
            "push": 0,
            "payload-type": "JSON",
            "devices": ["DHT-11"]
        })

        self.assertEqual(a.Wait, 1)

   
if __name__ == '__main__':
    unittest.main()        