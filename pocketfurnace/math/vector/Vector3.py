import math
from pocketfurnace.math.utils.Facing import Facing
from pocketfurnace.math.vector.Vector2 import Vector2


class Vector3:
    x = None
    y = None
    z = None

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_z(self) -> float:
        return self.z

    def get_floor_x(self) -> int:
        return int(math.floor(self.x))

    def get_floor_y(self) -> int:
        return int(math.floor(self.y))

    def get_floor_z(self) -> int:
        return int(math.floor(self.z))

    def add(self, x: float, y: float, z: float):
        return Vector3(self.x + x, self.y + y, self.z + z)

    def add_vector(self, vector):
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)

        return self.add(vector.x, vector.y, vector.z)

    def subtract(self, x: float, y: float, z: float):
        return self.add(-x, -y, -z)

    def subtract_vector(self, vector):
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)
        return self.add(-vector.x, -vector.y, -vector.z)

    def multiply(self, number):
        return Vector3(self.x * number, self.y * number, self.z * number)

    def divide(self, number):
        return Vector3(self.x / number, self.y / number, self.z / number)

    def ceil(self):
        return Vector3(int(math.ceil(self.x)), int(math.ceil(self.y)), int(math.ceil(self.z)))

    def floor(self):
        return Vector3(int(math.floor(self.x)), int(math.floor(self.y)), int(math.floor(self.z)))

    def round(self, precision=0):
        if precision > 0:
            return Vector3(round(self.x, precision), round(self.y, precision), round(self.z, precision))
        else:
            return Vector3(int(round(self.x, precision)), int(round(self.y, precision)), int(round(self.z, precision)))

    def abs(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def get_side(self, side: int, step=1):
        if side == Facing.DOWN:
            return Vector3(self.x, self.y - step, self.z)
        elif side == Facing.UP:
            return Vector3(self.x, self.y + step, self.z)
        elif side == Facing.NORTH:
            return Vector3(self.x, self.y, self.z - step)
        elif side == Facing.SOUTH:
            return Vector3(self.x, self.y, self.z + step)
        elif side == Facing.WEST:
            return Vector3(self.x - step, self.y, self.z)
        elif side == Facing.EAST:
            return Vector3(self.x + step, self.y, self.z)

    def down(self, step=1):
        return self.get_side(Facing.DOWN, step)

    def up(self, step=1):
        return self.get_side(Facing.UP, step)

    def north(self, step=1):
        return self.get_side(Facing.NORTH, step)

    def south(self, step=1):
        return self.get_side(Facing.SOUTH, step)

    def west(self, step=1):
        return self.get_side(Facing.WEST, step)

    def east(self, step=1):
        return self.get_side(Facing.EAST, step)

    # Yields vectors stepped out from this one in all directions.
    def sides(self, step=1):
        for facing in Facing.ALL:
            yield self.get_side(facing, step)

    # Same as sides() but returns a pre-populated array instead of Generator.
    def sides_array(self, step=1):
        return iter(self.sides(step))

    # Yields vectors stepped out from this one in directions except those on the given axis.
    def sides_around_axis(self, axis: int, step=1):
        for facing in Facing.ALL:
            if Facing.axis(facing) != axis:
                yield self.get_side(facing, step)

    def as_vector3(self):
        return Vector3(self.x, self.y, self.z)

    def distance(self, pos) -> float:
        if not isinstance(pos, Vector3):
            print("[PocketFurnace]: Invalid argument pos= " + pos)

        return math.sqrt(self.distance_squared(pos))

    def distance_squared(self, pos) -> float:
        if not isinstance(pos, Vector3):
            print("[PocketFurnace]: Invalid argument pos= " + str(pos))

        return float(((self.x - pos.x) ** 2) + ((self.y - pos.y) ** 2) + ((self.z - pos.z) ** 2))

    def max_plain_distance(self, x, z):
        if isinstance(x, Vector3):
            return self.max_plain_distance(x.x, x.z)
        elif isinstance(x, Vector2):  # reformat with Vector2
            return self.max_plain_distance(x.x, x.y)
        else:
            return max(abs(self.x - x), abs(self.z - z))

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def length_squared(self) -> float:
        return float(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.length_squared()
        if length > 0:
            return self.divide(math.sqrt(length))
        else:
            return Vector3(0, 0, 0)

    def dot(self, vector):
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)

        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def cross(self, vector):
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)

        return Vector3(
            self.y * vector.z - self.z * vector.y,
            self.z * vector.x - self.x * vector.z,
            self.x * vector.y - self.y * vector.x
        )

    def equals(self, vector) -> bool:
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)

        return self.x == vector.x and self.y == vector.y and self.z == vector.z

    # Returns a new vector with x value equal to the second parameter, along the line between this vector and the
    # passed in vector, or null if not possible.
    def get_intermediate_with_x_value(self, vector, x: float):
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)

        xDiff = vector.x - self.x
        if (xDiff * xDiff) < 0.0000001:
            return None
        f = (x - self.x) / xDiff
        if f < 0 or f > 1:
            return None
        else:
            return Vector3(x, self.y + (vector.y - self.y) * f, self.z + (vector.z - self.z) * f)

    # Returns a new vector with y value equal to the second parameter, along the line between this vector and the
    # passed in vector, or null if not possible.
    def get_intermediate_with_y_value(self, vector, y: float):
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)

        yDiff = vector.y - self.y
        if (yDiff * yDiff) < 0.0000001:
            return None
        f = (y - self.y) / yDiff
        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + (vector.x - self.x) * f, y, self.z + (vector.z - self.z) * f)

    # Returns a new vector with z value equal to the second parameter, along the line between this vector and the
    # passed in vector, or null if not possible.
    def get_intermediate_with_z_value(self, vector, z: float):
        if not isinstance(vector, Vector3):
            print("[PocketFurnace]: Invalid argument vector= " + vector)

        zDiff = vector.z - self.z
        if (zDiff * zDiff) < 0.0000001:
            return None
        f = (z - self.z) / zDiff
        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + (vector.x - self.x) * f, self.y + (vector.y - self.y) * f, z)

    def set_components(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        return self

    def to_string(self) -> str:
        return "Vector3(x=" + str(self.x) + ",y=" + str(self.y) + ",z=" + str(self.z) + ")"
