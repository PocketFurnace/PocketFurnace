class Facing:
    AXIS_Y = 0
    AXIS_Z = 1
    AXIS_X = 2

    FLAG_AXIS_POSITIVE = 1

    # most significant 2 bits = axis, least significant bit = is positive direction
    DOWN = AXIS_Y << 1
    UP = (AXIS_Y << 1) | FLAG_AXIS_POSITIVE
    NORTH = AXIS_Z << 1
    SOUTH = (AXIS_Z << 1) | FLAG_AXIS_POSITIVE
    WEST = AXIS_X << 1
    EAST = (AXIS_X << 1) | FLAG_AXIS_POSITIVE

    ALL = [
        DOWN,
        UP,
        NORTH,
        SOUTH,
        WEST,
        EAST
    ]

    HORIZONTAL = [
        NORTH,
        SOUTH,
        WEST,
        EAST
    ]

    CLOCKWISE = {
        AXIS_Y: {
            NORTH: EAST,
            EAST: SOUTH,
            SOUTH: WEST,
            WEST: NORTH
        },
        AXIS_Z: {
            UP: EAST,
            EAST: DOWN,
            DOWN: WEST,
            WEST: UP
        },
        AXIS_X: {
            UP: NORTH,
            NORTH: DOWN,
            DOWN: SOUTH,
            SOUTH: UP
        }
    }

    # Returns the axis of the given direction.
    @staticmethod
    def axis(direction: int) -> int:
        return int(direction >> 1)  # shift off positive/negative bit

    # Returns whether the direction is facing the positive of its axis.
    @staticmethod
    def is_positive(direction: int) -> bool:
        return bool((direction & Facing.FLAG_AXIS_POSITIVE) == Facing.FLAG_AXIS_POSITIVE)

    # Returns the opposite Facing of the specified one.
    @staticmethod
    def opposite(direction: int) -> int:
        return int(direction ^ Facing.FLAG_AXIS_POSITIVE)

    # Rotates the given direction around the axis.
    @staticmethod
    def rotate(direction: int, axis: int, clockwise: bool) -> int:
        if axis not in Facing.CLOCKWISE:
            print("[PocketFurnace]: Invalid axis " + str(axis))
        if direction not in Facing.CLOCKWISE[axis]:
            print("[PocketFurnace]: Cannot rotate direction $direction around axis " + str(axis))

        rotated = Facing.CLOCKWISE[axis][direction]
        if clockwise:
            return rotated
        else:
            return Facing.opposite(rotated)

    @staticmethod
    def rotate_y(direction: int, clockwise: bool) -> int:
        return Facing.rotate(direction, Facing.AXIS_Y, clockwise)

    @staticmethod
    def rotate_z(direction: int, clockwise: bool) -> int:
        return Facing.rotate(direction, Facing.AXIS_Z, clockwise)

    @staticmethod
    def rotate_x(direction: int, clockwise: bool) -> int:
        return Facing.rotate(direction, Facing.AXIS_X, clockwise)

    # Validates the given integer as a Facing direction.
    @staticmethod
    def validate(facing: int):
        if facing not in Facing.ALL:
            print("[PocketFurnace]: Invalid direction " + str(facing))
