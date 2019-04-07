import unittest
import logging
import platform

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")

from demo.devices.linux_cpu_temp import CpuTemp

class CpuTemp_Tests(unittest.TestCase):
    def test_temp(self):
        cpu = CpuTemp()
        a = cpu.read()
        if platform.machine() != 'x86_64':
            self.assertTrue(a > 0)
        else:
            self.assertEqual(a, 0)