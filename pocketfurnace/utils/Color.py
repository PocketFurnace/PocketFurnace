class Color:
    """
    Provide useful utils to manage rgb and rba colors
    """
    _a = None
    _r = None
    _g = None
    _b = None

    def __init__(self, r: int, g: int, b: int, a=0xff):
        self._r = r
        self._g = g
        self._b = b
        self._a = a

    def get_a(self) -> int:
        return self._a

    def set_a(self, a: int) -> None:
        self._a = a & 0xff

    def get_r(self) -> int:
        return self._r

    def set_r(self, r: int) -> None:
        self._r = r & 0xff

    def get_g(self) -> int:
        return self._g

    def set_g(self, g: int) -> None:
        self._g = g & 0xff

    def get_b(self) -> int:
        return self._b

    def set_b(self, b: int) -> None:
        self._b = b & 0xff

    @classmethod
    def mix(cls, *args):
        count = len(args)
        if count < 1:
            raise TypeError("Please provide colors")
        a = r = g = b = 0
        for color in args:
            a = a + color.a
            r = r + color.r
            g = g + color.g
            b = b + color.b
        return cls(int(r / count), int(g / count), int(b / count), int(a / count))

    @classmethod
    def from_rgb(cls, code: int):
        return cls((code >> 16) & 0xff, (code >> 8) & 0xff, code & 0xff)

    @classmethod
    def from_argb(cls, code: int):
        return cls((code >> 16) & 0xff, (code >> 8) & 0xff, code & 0xff, (code >> 24) & 0xff)

    def to_argb(self) -> int:
        return (self._a << 24) | (self._r << 16) | (self._g << 8) | self._b

    def to_bgra(self) -> int:
        return (self._b << 24) | (self._g << 16) | (self._r << 8) | self._a

    def to_rgba(self) -> int:
        return (self._r << 24) | (self._g << 16) | (self._b << 8) | self._a

    def to_abgr(self) -> int:
        return (self._a << 24) | (self._b << 16) | (self._g << 8) | self._r

    @classmethod
    def from_abgr(cls, code: int):
        return cls(code & 0xff, (code >> 8) & 0xff, (code >> 16) & 0xff, (code >> 24) & 0xff)
