import psutil
import logging
import time
logger = logging.getLogger(__name__)

from demo.devices.devicebase import DeviceBase
from demo.devices.deviceresult import DeviceResult
from demo.devices.devicetype import DeviceType

class MemoryInfo(DeviceBase):
    def __init__(self, config):
        super().__init__(config, DeviceType.MEMORY)

    def read(self):
        start = time.time()
        result = DeviceResult(super().Config.Name, 0.0, False)
        try:
            mem = psutil.virtual_memory()            
            swap = psutil.swap_memory()
            end = time.time()
            result.Duration = (end - start)
            result.add_reading("Total","float",mem.total)
            result.add_reading("Available","float",mem.available)
            result.add_reading("Swap Total", "float",swap.total)
            result.add_reading("SWap Available", "float",swap.free)
            result.IsValid = True

        except:
            logger.warn("Problem with reading CPU Percentage!")
        return result