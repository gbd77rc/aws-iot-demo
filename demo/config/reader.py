import json
import os
import errno
import logging

logger = logging.getLogger(__name__)

class Reader:
    __config_file = ""

    def __init__(self, config_file):
        if os.path.isfile(config_file) == False:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_file)
        self.__config_file = config_file
        logger.debug("Initialized with config file set to {}".format(config_file))


    def read(self):
        with open(self.__config_file) as config_file:
            config = json.load(config_file)
        logger.debug("Configuration is [{}]".format(json.dumps(config)))
        return config