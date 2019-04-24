from enum import Enum
import logging
logger = logging.getLogger(__name__)

class DirectionType(Enum):
    DIRNONE = 0
    IN = 1
    OUT = 2
    BOTH = 3

    @staticmethod
    def get_type(name):
        if name.upper() == "IN":
            return DirectionType.IN
        if name.upper() == "OUT":
            return DirectionType.OUT
        if name.upper() == "BOTH":
            return DirectionType.BOTH
        return DirectionType.DIRNONE

    def __eq__(self, other):
        return self.value == other.value
