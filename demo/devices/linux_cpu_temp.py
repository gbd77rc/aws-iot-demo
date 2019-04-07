import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CpuTemp:
    __fsyspath = '/sys/class/thermal/thermal_zone0/temp'

    def read(self):
        temp = Path(self.__fsyspath)
        if temp.is_file():
            with open(self.__fsyspath) as fid:
                value = int(fid.readline())
                logger.debug("CPU Temperature is {}".format(value/1000))
                return value/1000
        return 0