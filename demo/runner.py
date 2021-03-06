import logging
import sys
import platform
if platform.machine() == 'x86_64':
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
    fake_rpi.toggle_print(False)


import getopt

from demo.telemetry.sensor import Sensor
from demo.config.reader import Reader
from demo.control.lights import Lights
from demo.shadow.service import Service

def startup(argv):
    try:
        opts, _ = getopt.getopt(argv, "hc:s:",["config=","sensors="])
    except getopt.GetoptError:
        print("error: runner.py -c <config_file>")
        sys.exit(2)

    if len(opts) == 0:
        print("missing configuration file:  runner.py -c <config_file>")
        sys.exit(2)

    config_file = ""
    publish_temp = True
    for opt, arg in opts:
        if opt == '-h':
            print("runner.py -c <config_file>")
            sys.exit()
        if opt in ('-c', '--config'):
            config_file = arg
        if opt in ('-s', '--sensors'):
            publish_temp = True if arg.lower() in ('on', 'yes') else False

    config_reader = Reader(config_file)
    config = config_reader.read()

    numeric_level = getattr(logging, config["logging"]["level"].upper(), None)
    logging.basicConfig(level=numeric_level,
                        format="%(asctime)s - %(name)s - %(levelname)s - [%(message)s]")
    logger = logging.getLogger("Demo Telemetry")    
    logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")                        

    fileHandler = logging.FileHandler(config["logging"]["location"])
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.ERROR)   

    logger.info("Starting Demo")
    logger.info("Logging Level is set to {}".format(config["logging"]["level"]))
    logger.info("Publishing Sensors is {}".format("ON" if publish_temp else "OFF"))

    shadow = Service(config)
    lights = Lights(config)
    lights.register(shadow)
    lights.subscribe()
    
    sensor = Sensor(config)
        
    if publish_temp:
        sensor.register(shadow)
        sensor.start()
    shadow.start()
    logger.info("To Exit press <enter>")
    input()
    if publish_temp:
        sensor.stop()
    lights.unsubscribe()
    shadow.stop()
    logger.info("Completed the demo!")

if __name__ == "__main__":
    startup(sys.argv[1:])                 