from demo.devices.cpu_precent import CpuPercent
import unittest
import logging
import platform
from demo.config.deviceconfig import DeviceConfig

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")


class CpuPercent_Tests(unittest.TestCase):
    def test_percentage(self):
        config = DeviceConfig({
            "type": "cpupercent",
            "name": "CPU Percentage"
        })
        cpu = CpuPercent(config)
        a = cpu.read()
        self.assertTrue(a.IsValid)
        logging.info("Reading is {}".format(a.to_json(pretty=True)))
    
    def test_dif_config_type(self):
        config = DeviceConfig({
            "type": "memory",
            "name": "Memory"
        })

        self.assertRaises(ValueError, CpuPercent, config)


if __name__ == '__main__':
    unittest.main()        