import unittest
import logging
import time
import sys
import platform
if platform.machine() == 'x86_64':
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi     # Fake RPi (GPIO)
    fake_rpi.toggle_print(False)

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")
from demo.devices.led import Led
from demo.config.deviceconfig import DeviceConfig
from demo.devices.directiontype import DirectionType

class LED_Tests(unittest.TestCase):
    green_led = {}
    def setUp(self):
        self.config = DeviceConfig({
            "name": "Green",
            "type": "led",
            "pin": 6
        })
        self.green_led = Led(self.config)

    def test_on(self):
        self.green_led.on()
        state = self.green_led.get_state()
        logging.debug("State is {}".format(state))
        self.assertEqual(state["green"], "on")
        self.green_led.off()

    def test_off(self):
        self.green_led.on()
        state = self.green_led.get_state()
        self.assertEqual(state["green"], "on")
        self.green_led.off()
        state = self.green_led.get_state()
        self.assertEqual(state["green"], "off")

    def test_blink(self):
        self.green_led.blink_on(500)
        time.sleep(2)
        state = self.green_led.get_state()
        logging.debug("State is {}".format(state))
        self.assertTrue(self.green_led.is_blinking())
        self.green_led.blink_off()
        time.sleep(1)
        state = self.green_led.get_state()
        self.assertEqual(state["green"], "off")
        self.assertFalse(self.green_led.is_blinking())
        
    def test_write(self):
        self.green_led.write(1)
        self.assertTrue(self.green_led.is_on())
        self.green_led.write(0)
        self.assertFalse(self.green_led.is_on())
        self.assertEqual(self.green_led.Direction, DirectionType.OUT)
        
    def test_dif_config_type(self):
        config = DeviceConfig({
            "type": "memory",
            "name": "Memory"
        })

        self.assertRaises(ValueError, Led, config)
        
if __name__ == '__main__':
    unittest.main()