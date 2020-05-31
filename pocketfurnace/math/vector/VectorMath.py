import abc
import math

from pocketfurnace.math.vector.Vector2 import Vector2


class VectorMath(metaclass=abc.ABCMeta):
    @staticmethod
    def get_direction_2d(azimuth: float):
        return Vector2(math.cos(azimuth), math.sin(azimuth))
