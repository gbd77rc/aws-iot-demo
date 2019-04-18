from demo.devices.linux_cpu_temp import CpuTemp
import unittest
import logging
import platform
from demo.config.deviceconfig import DeviceConfig

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")


class CpuTemp_Tests(unittest.TestCase):
    def test_temp(self):
        config = DeviceConfig({
            "type": "cputemp",
            "name": "CPU Temperature",
            "location": "/sys/class/thermal/thermal_zone0/temp"
        })
        cpu = CpuTemp(config)
        a = cpu.read()
        if platform.machine() != 'x86_64':
            self.assertTrue(a.IsValid)
        else:
            self.assertFalse(a.IsValid)
    
    def test_dif_config_type(self):
        config = DeviceConfig({
            "type": "memory",
            "name": "Memory"
        })

        self.assertRaises(ValueError, CpuTemp, config)