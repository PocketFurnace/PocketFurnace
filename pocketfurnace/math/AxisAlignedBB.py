from copy import deepcopy
from pocketfurnace.math.utils.Facing import Facing
from pocketfurnace.math.vector.Vector3 import Vector3


class AxisAlignedBB:
    min_x = None
    min_y = None
    min_z = None
    max_x = None
    max_y = None
    max_z = None

    def __init__(self, minx: float, miny: float, minz: float, maxx: float, maxy: float, maxz: float):
        if minx > maxx:
            print("minX " + str(minx) + "is larger than maxX " + str(maxx))

        if miny > maxy:
            print("minY " + str(miny) + "is larger than maxY " + str(maxy))

        if minz > maxz:
            print("minZ " + str(minz) + "is larger than maxZ " + str(maxz))

        self.min_x = minx
        self.min_y = miny
        self.min_z = minz
        self.max_x = maxx
        self.max_y = maxy
        self.max_z = maxz

    # Returns a new AxisAlignedBB extended by the specified X, Y and Z.
    # If each of X, Y and Z are positive, the relevant max bound will be increased. If negative, the relevant min
    # bound will be decreased.
    def add_coord(self, x: float, y: float, z: float):
        minx = self.min_x
        miny = self.min_y
        minz = self.min_z
        maxx = self.max_x
        maxy = self.max_y
        maxz = self.max_z

        if x < 0:
            minx += x
        elif x > 0:
            maxx += x

        if y < 0:
            miny += y
        elif y > 0:
            maxy += y

        if z < 0:
            minz += y
        elif z > 0:
            maxz += z

        return AxisAlignedBB(minx, miny, minz, maxx, maxy, maxz)

    # Outsets the bounds of this AxisAlignedBB by the specified X, Y and Z.
    def expand(self, x: float, y: float, z: float):
        self.min_x -= x
        self.min_y -= y
        self.min_z -= z
        self.max_x += x
        self.max_y += y
        self.max_z += z
        return self

    # Returns an expanded clone of this AxisAlignedBB.
    def expanded_copy(self, x: float, y: float, z: float):
        return deepcopy(self).expand(x, y, z)

    # Shifts this AxisAlignedBB by the given X, Y and Z.
    def offset(self, x: float, y: float, z: float):
        self.min_x += x
        self.min_y += y
        self.min_z += z
        self.max_x += x
        self.max_y += y
        self.max_z += z
        return self

    # Returns an offset clone of this AxisAlignedBB.
    def offset_copy(self, x: float, y: float, z: float):
        return deepcopy(self).offset(x, y, z)

    # Insets the bounds of this AxisAlignedBB by the specified X, Y and Z.
    def contract(self, x: float, y: float, z: float):
        self.min_x += x
        self.min_y += y
        self.min_z += z
        self.max_x -= x
        self.max_y -= y
        self.max_z -= z
        return self

    # Returns a contracted clone of this AxisAlignedBB.
    def contracted_copy(self, x: float, y: float, z: float):
        return deepcopy(self).contract(x, y, z)

    # Extends the AABB in the given direction.
    def extend(self, face: int, distance: float):
        if face == Facing.DOWN:
            self.min_y -= distance
        elif face == Facing.UP:
            self.max_y += distance
        elif face == Facing.NORTH:
            self.min_z -= distance
        elif face == Facing.SOUTH:
            self.max_z += distance
        elif face == Facing.WEST:
            self.min_x -= distance
        elif face == Facing.EAST:
            self.max_x += distance
        else:
            print("[PocketFurnace]: Invalid face " + str(face))
        return self

    # Returns an extended clone of this bounding box.
    def extended_copy(self, face: int, distance: float):
        return deepcopy(self).extend(face, distance)

    # Inverse of extend().
    def trim(self, face: int, distance: float):
        return self.extend(face, -distance)

    # Returns a trimmed clone of this bounding box.
    def trimmed_copy(self, face: int, distance: float):
        return self.extended_copy(face, -distance)

    # Increases the dimension of the AABB along the given axis.
    def stretch(self, axis: int, distance: float):
        if axis == Facing.AXIS_Y:
            self.min_y -= distance
            self.max_y += distance
        elif axis == Facing.AXIS_Z:
            self.min_z -= distance
            self.max_z += distance
        elif axis == Facing.AXIS_X:
            self.min_x -= distance
            self.max_x += distance
        else:
            print("[PocketFurnace]: Invalid axis " + str(axis))
        return self

    # Returns a stretched copy of this bounding box.
    def stretched_copy(self, axis: int, distance: float):
        return deepcopy(self).stretch(axis, distance)

    # Reduces the dimension of the AABB on the given axis. Inverse of stretch().
    def squash(self, axis: int, distance: float):
        return self.stretch(axis, -distance)

    # Returns a squashed copy of this bounding box.
    def squashed_copy(self, axis: int, distance: float):
        return self.stretched_copy(axis, -distance)

    def calculate_x_offset(self, bb, x: float) -> float:
        if bb.max_y <= self.min_y or bb.min_y >= self.max_y:
            return x
        if bb.max_z <= self.min_z or bb.min_z >= self.max_z:
            return x
        if x > 0 and bb.max_x <= self.min_x:
            x1 = self.min_x - bb.max_x
            if x1 < x:
                x = x1
        elif x < 0 and bb.min_x >= self.max_x:
            x2 = self.max_x - bb.min_x
            if x2 > x:
                x = x2
        return x

    def calculate_y_offset(self, bb, y) -> float:
        if bb.max_x <= self.min_x or bb.min_x >= self.max_x:
            return y
        if bb.max_z <= self.min_z or bb.min_z >= self.max_z:
            return y
        if y > 0 and bb.max_y <= self.min_y:
            y1 = self.min_y - bb.max_y
            if y < y1:
                y = y1
        elif y < 0 and bb.min_y >= self.max_y:
            y2 = self.max_y - bb.min_y
            if y2 > y:
                y = y2
        return y

    def calculate_z_offset(self, bb, z) -> float:
        if bb.max_x <= self.min_x or bb.min_x >= self.max_x:
            return z
        if bb.max_y <= self.min_y or bb.min_y >= self.max_y:
            return z
        if z > 0 and bb.max_z <= self.min_z:
            z1 = self.min_z - bb.max_z
            if z1 < z:
                z = z1
        elif z < 0 and bb.min_z >= self.max_z:
            z2 = self.max_z - bb.min_z
            if z2 > z:
                z = z2
        return z

    # Returns whether any part of the specified AABB is inside (intersects with) this one.
    def intersects_with(self, bb, epsilon=0.00001) -> bool:
        if bb.max_x - self.min_x > epsilon and self.max_x - bb.min_x > epsilon:
            if bb.max_y - self.min_y > epsilon and self.max_y - bb.min_y > epsilon:
                return bb.max_z - self.min_z > epsilon and self.max_z - bb.min_z > epsilon
        return False

    # Returns whether the specified vector is within the bounds of this AABB on all axes.
    def is_vector_inside(self, vector: Vector3) -> bool:
        if vector.x <= self.min_x or vector.x >= self.max_x:
            return False
        if vector.y <= self.min_y or vector.y >= self.max_y:
            return False
        return vector.z > self.min_z and vector.z < self.max_z

    # Returns the mean average of the AABB's X, Y and Z lengths.
    def get_average_edge_length(self) -> float:
        return float((self.max_x - self.min_x + self.max_y - self.min_y + self.max_z - self.min_z) / 3)

    # Returns the interior volume of the AABB.
    def get_volume(self) -> float:
        return float((self.max_x - self.min_x) * (self.max_y - self.min_y) * (self.max_z - self.min_z))

    # Returns whether the specified vector is within the Y and Z bounds of this AABB.
    def is_vector_in_yz(self, vector: Vector3) -> bool:
        return vector.y >= self.min_y and vector.y <= self.max_y and vector.z >= self.min_z and vector.z <= self.max_z

    # Returns whether the specified vector is within the X and Z bounds of this AABB.
    def is_vector_in_xz(self, vector: Vector3) -> bool:
        return vector.x >= self.min_x and vector.x <= self.max_x and vector.z >= self.min_z and vector.z <= self.max_z

    # Returns whether the specified vector is within the X and Y bounds of this AABB.
    def is_vector_in_xy(self, vector: Vector3) -> bool:
        return vector.x >= self.min_x and vector.x <= self.max_x and vector.y >= self.min_y and vector.y <= self.max_y

    def to_string(self) -> str:
        min = str(self.min_x) + ", " + str(self.min_y) + ", " + str(self.min_z)
        max = str(self.max_x) + ", " + str(self.max_y) + ", " + str(self.max_z)
        return "AxisAlignedBB(" + min + ", " + max + ")"

    # Returns a 1x1x1 bounding box starting at grid position 0,0,0.
    @staticmethod
    def one():
        return AxisAlignedBB(0, 0, 0, 1, 1, 1)
