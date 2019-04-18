from demo.devices.cpu_precent import CpuPercent
import unittest
import logging
import platform
from demo.config.deviceconfig import DeviceConfig

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")


class CpuTemp_Tests(unittest.TestCase):
    def test_percentage(self):
        config = DeviceConfig({
            "type": "cpupercent",
            "name": "CPU Percentage",
            "location": "/sys/class/thermal/thermal_zone0/temp"
        })
        cpu = CpuPercent(config)
        a = cpu.read()
        self.assertTrue(a.IsValid)
        logging.info("Reading is {}".format(a.to_json(pretty=True)))