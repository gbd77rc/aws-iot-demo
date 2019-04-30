import unittest
import logging
import time
import sys
import json

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.config.providerconfig import ProviderConfig

class ProviderConfig_Tests(unittest.TestCase):
    def test_type_exception(self):
        self.assertRaises(TypeError, ProviderConfig, None)

    def test_value_exception(self):
        self.assertRaises(ValueError, ProviderConfig, {})
        self.assertRaises(ValueError, ProviderConfig, {
            "type": "Test-1",
            "endpoint": "",
            "thing_id": ""
        })
        self.assertRaises(ValueError, ProviderConfig, {
            "type": "Test-1",
            "endpoint": "test1",
            "thing_id": ""
        })

    def test_find_security(self):
        a = ProviderConfig({
            "type":"test1",
            "endpoint": "test2",
            "thing_id": "test3",
            "client_id": "test4",
            "port":8883,
            "security":[{"a":"a1"}, {"b": "b1"}],
            "mode": "STAND"
        })

        b = a.get_security_key("b")
        logging.info("Security = {}".format(b))
        self.assertEqual(b["b"], "b1")


if __name__ == '__main__':
    unittest.main()        