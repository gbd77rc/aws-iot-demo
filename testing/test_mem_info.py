from demo.devices.memory_load import MemoryInfo
import unittest
import logging
import platform
from demo.config.deviceconfig import DeviceConfig

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")


class MemoryInfo_Tests(unittest.TestCase):
    def test_memory(self):
        config = DeviceConfig({
            "type": "memory",
            "name": "Memory Information"
        })
        mem = MemoryInfo(config)
        a = mem.read()
        self.assertTrue(a.IsValid)
        logging.info("Reading is {}".format(a.to_json(pretty=True)))

    def test_dif_config_type(self):
        config = DeviceConfig({
            "type": "cputemp",
            "name": "CPU"
        })

        self.assertRaises(ValueError, MemoryInfo, config)