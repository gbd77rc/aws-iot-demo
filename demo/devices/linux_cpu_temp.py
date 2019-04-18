import time
from demo.config.deviceconfig import DeviceConfig
from demo.devices.devicebase import DeviceBase
from demo.devices.deviceresult import DeviceResult

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CpuTemp(DeviceBase):
    def __init__(self, config):
        super().__init__(config)

    def read(self):
        temp = Path(super().Config.Location)
        result = DeviceResult(super().Config.Name, 0.0, False)

        if temp.is_file():
            start = time.time()
            with temp.open() as fid:
                value = int(fid.readline())
                end = time.time()
                logger.debug("CPU Temperature is {}".format(value/1000.0))
                result.IsValid = True
                result.Duration = (end - start)
                result.add_reading("CPU Temperature", "float", value/1000.0)
        return result