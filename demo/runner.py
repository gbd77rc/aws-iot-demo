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


def startup(argv):
    try:
        opts, _ = getopt.getopt(argv, "hc:",["config="])
    except getopt.GetoptError:
        print("error: runner.py -c <config_file>")
        sys.exit(2)

    if len(opts) == 0:
        print("missing configuration file:  runner.py -c <config_file>")
        sys.exit(2)

    config_file = ""
    for opt, arg in opts:
        if opt == '-h':
            print("runner.py -c <config_file>")
            sys.exit()
        if opt in ('-c', '--config'):
            config_file = arg

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

    sensor = Sensor(config)
    sensor.start()
    lights = Lights(config)
    lights.subscribe()
    logger.info("To Exit press <enter>")
    input()
    sensor.stop()
    lights.unsubscribe()
    logger.info("Completed the demo!")

if __name__ == "__main__":
    startup(sys.argv[1:])                 