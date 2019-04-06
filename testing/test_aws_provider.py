import unittest
import logging
import time
import sys

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")
from demo.provider.aws import AwsProvider

class AwsProvider_Tests(unittest.TestCase):
    config = {}
    def setUp(self):
        self.config = {
            "aws": {
                "telemetry_topic": "telemetry/rpi-1",
                "control_topic": "control/rpi-1",
                "client_id": "rpi-1",
                "shadow_id": "iot-demo-rpi-1",
                "endpoint": "a1bqyju1450wf9-ats.iot.eu-west-1.amazonaws.com",
                "port": 8883,
                "root": "./certs/root-ca.pem",
                "cert": "./certs/8098cdfe96-certificate.pem.crt",
                "private": "./certs/8098cdfe96-private.pem.key"
            }
        }

    def test_get_client(self):
        provider =  AwsProvider(self.config)
        client = provider.get_client()
        self.assertIsNotNone(client)

    def test_get_shadow_handle(self):
        provider =  AwsProvider(self.config)
        client = provider.get_shadow_handle()
        self.assertIsNotNone(client)        

    def test_same_instance(self):
        p1 = AwsProvider(self.config)
        p2 = AwsProvider(self.config)

        self.assertEqual(p1.__repr__(), p2.__repr__())
        

if __name__ == '__main__':
    unittest.main()