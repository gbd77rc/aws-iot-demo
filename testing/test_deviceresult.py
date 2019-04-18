import unittest
import logging
import time
import sys
import json

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.devices.deviceresult import DeviceResult

class DeviceResult_Tests(unittest.TestCase):
    def test_check_multiple(self):
        dr = DeviceResult("Test-1", 0.5)
        dr.add_reading("Temp1", "float", 56.0)
        dr.add_reading("Temp2", "float", 58.0)

        js = dr.to_json()

        obj = json.loads(js)
        self.assertEqual(obj["name"], "Test-1")
        self.assertEqual(len(obj["readings"]), 2)
        self.assertEqual(obj["isvalid"], True)
        self.assertEqual(obj["readings"][0]["value"], 56.0)    
        self.assertEqual(obj["readings"][1]["value"], 58.0)

    def test_check_duplicates(self):
        dr = DeviceResult("Test-1", 0.5)
        dr.add_reading("Temp1", "float", 56.0)
        dr.add_reading("Temp1", "float", 58.0)

        js = dr.to_json()

        obj = json.loads(js)
        self.assertEqual(obj["name"], "Test-1")
        self.assertEqual(len(obj["readings"]), 1)
        self.assertEqual(obj["readings"][0]["value"], 58.0)

    def test_check_json(self):
        dr = DeviceResult("Test-1", 0.5)
        js = dr.to_json()
        expected = "{\"name\":\"Test-1\",\"duration\":0.5,\"isvalid\":true,\"readings\":[]}"
        self.assertEqual(js, expected)    

    def test_check_json_pretty(self):
        dr = DeviceResult("Test-1", 0.5)
        js = dr.to_json(True)
        expected = "{\n    \"duration\": 0.5,\n    \"isvalid\": true,\n    \"name\": \"Test-1\",\n    \"readings\": []\n}"
        self.assertEqual(js, expected)   


if __name__ == '__main__':
    unittest.main()        