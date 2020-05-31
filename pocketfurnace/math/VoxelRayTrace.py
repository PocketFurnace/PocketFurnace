import abc
import math
from pocketfurnace.math.vector.Vector3 import Vector3


class VoxelRayTrace(metaclass=abc.ABCMeta):
    @staticmethod
    def in_direction(start: Vector3, directionVector: Vector3, maxDistance: float):
        return VoxelRayTrace.between_points(start, start.add_vector(directionVector.multiply(maxDistance)))

    @staticmethod
    def between_points(start: Vector3, end: Vector3):
        currentBlock = start.floor()
        directionVector = end.subtract_vector(start).normalize()
        if directionVector.length_squared() <= 0:
            print("[PocketFurnace]: Start and end points are the same, giving a zero direction vector")

        radius = start.distance(end)

        stepX = VoxelRayTrace.spaceshift(directionVector.x, 0)
        stepY = VoxelRayTrace.spaceshift(directionVector.y, 0)
        stepZ = VoxelRayTrace.spaceshift(directionVector.z, 0)

        # Initialize the step accumulation variables depending how far into the current block the start position is. If
        # the start position is on the corner of the block, these will be zero.
        tMaxX = VoxelRayTrace.ray_trace_distance_to_boundary(start.x, directionVector.x)
        tMaxY = VoxelRayTrace.ray_trace_distance_to_boundary(start.y, directionVector.y)
        tMaxZ = VoxelRayTrace.ray_trace_distance_to_boundary(start.z, directionVector.z)

        # The change in t on each axis when taking a step on that axis (always positive).

        if directionVector.x == 0:
            tDeltaX = 0
        else:
            tDeltaX = stepX / directionVector.x
        if directionVector.y == 0:
            tDeltaY = 0
        else:
            tDeltaY = stepY / directionVector.y
        if directionVector.z == 0:
            tDeltaZ = 0
        else:
            tDeltaZ = stepZ / directionVector.z

        loop = True

        while loop:
            yield currentBlock

            # tMaxX stores the t-value at which we cross a cube boundary along the
            # X axis, and similarly for Y and Z. Therefore, choosing the least tMax
            # chooses the closest cube boundary

            if tMaxX < tMaxY and tMaxX < tMaxZ:
                if tMaxX > radius:
                    break
                currentBlock.x += stepX
                tMaxX += tDeltaX
            elif tMaxY < tMaxZ:
                if tMaxY > radius:
                    break
                currentBlock.y += stepY
                tMaxY += tDeltaY
            else:
                if tMaxZ > radius:
                    break
                currentBlock.z += stepZ
                tMaxZ += tDeltaZ

    # Returns the distance that must be travelled on an axis from the start point with the direction vector component
    # to cross a block boundary. For example, given an X coordinate inside a block and the X component of a direction
    # vector, will return the distance travelled by that direction component to reach a block with a different X
    # coordinate. Find the smallest positive t such that s+t*ds is an integer.
    @staticmethod
    def ray_trace_distance_to_boundary(s: float, ds: float) -> float:
        if ds == 0:
            return float('inf')

        if ds < 0:
            s = -s
            ds = -ds

            if math.floor(s) == s:  # exactly at coordinate, will leave the coordinate immediately by moving negatively
                return 0
        return (1 - (s - math.floor(s))) / ds

    @staticmethod
    def spaceshift(a, b):
        if a < b:
            return -1
        elif a == b:
            return 0
        elif a > b:
            return 1
