import math


class Vector2:
    x = None
    y = None

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_floor_x(self) -> int:
        return int(math.floor(self.x))

    def get_floor_y(self) -> int:
        return int(math.floor(self.y))

    def add(self, x, y: float):
        if isinstance(x, Vector2):
            return self.add(x.x, x.y)
        else:
            return Vector2(self.x + x, self.y + y)

    def subtract(self, x, y: float):
        if isinstance(x, Vector2):
            return self.add(-x.x, -x.y)
        else:
            return self.add(-x, -y)

    def ceil(self):
        return Vector2(int(math.ceil(self.x)), int(math.ceil(self.y)))

    def floor(self):
        return Vector2(int(math.floor(self.x)), int(math.floor(self.y)))

    def round(self):
        return Vector2(round(self.x), round(self.y))

    def abs(self):
        return Vector2(abs(self.x), abs(self.y))

    def multiply(self, number: float):
        return Vector2(self.x * number, self.y * number)

    def divide(self, number: float):
        return Vector2(self.x / number, self.y / number)

    def distance(self, x, y: float) -> float:
        if isinstance(x, Vector2):
            return math.sqrt(self.distance_squared(x.x, x.y))
        else:
            return math.sqrt(self.distance_squared(x, y))

    def distance_squared(self, x, y: float) -> float:
        if isinstance(x, Vector2):
            return self.distance_squared(x.x, x.y)
        else:
            return ((self.x - x) ** 2) + ((self.y - y) ** 2)

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalize(self):
        length = self.length_squared()
        if length > 0:
            return self.divide(math.sqrt(length))
        return Vector2(0, 0)

    def dot(self, vector) -> float:
        return self.x * vector.x + self.y * vector.y

    def to_string(self) -> str:
        return "Vector2(x=" + str(self.x) + ",y=" + str(self.y) + ")"