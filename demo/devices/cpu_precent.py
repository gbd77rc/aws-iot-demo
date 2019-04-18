import psutil
import logging
import time
logger = logging.getLogger(__name__)

from demo.devices.devicebase import DeviceBase
from demo.devices.deviceresult import DeviceResult

class CpuPercent(DeviceBase):
    def __init__(self, config):
        super().__init__(config)

    def read(self):
        start = time.time()
        result = DeviceResult(super().Config.Name, 0.0, False)
        try:
            cpu = psutil.cpu_percent()
            cpu_individual = psutil.cpu_percent(percpu=True)
            end = time.time()
            result.Duration = (end - start)
            result.add_reading("All CPU","float", cpu)
            count = 1
            for proc in cpu_individual:
                result.add_reading("CPU {}".format(count), "float", proc)
                count += 1

            result.IsValid = True

        except:
            logger.warn("Problem with reading CPU Percentage!")
        return result