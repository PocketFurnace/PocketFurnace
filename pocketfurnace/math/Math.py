import abc
import math


class Math(metaclass=abc.ABCMeta):
    @staticmethod
    def floor_float(n: float) -> int:
        i = int(n)
        if n >= i:
            return i
        else:
            return i - 1

    @staticmethod
    def ceil_float(n : float) -> int:
        i = int(n)
        if n <= i:
            return i
        else:
            return i + 1

    # Solves a quadratic equation with the given coefficients and returns an array of up to two solutions.
    @staticmethod
    def solve_quadratic(a: float, b: float, c: float):
        discriminant = b ** 2 - 4 * a * c
        if discriminant > 0:  # 2 real roots
            sqrtDiscriminant = math.sqrt(discriminant)
            return [
                (-b + sqrtDiscriminant) / (2 * a),
                (-b - sqrtDiscriminant) / (2 * a)
            ]
        elif discriminant == 0:  # 1 real root
            return [
                -b / (2 * a)
            ]
        else:  # No real roots
            return []
