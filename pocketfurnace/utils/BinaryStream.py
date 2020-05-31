import sys
from pprint import pprint
from pocketfurnace.utils.Binary import Binary


class BinaryDataException(Exception):
    pass


class BinaryStream:
    offset = 0
    buffer = b""

    def __init__(self, buffer: bytes = b"", offset: int = 0):
        self.buffer = buffer
        self.offset = offset

    def reset(self):
        self.buffer = b""
        self.offset = 0
        return self

    def rewind(self):
        self.offset = 0

    def set_offset(self, offset: int):
        self.offset = offset

    def set_buffer(self, buffer: bytes, offset: int = 0):
        self.buffer = buffer
        self.offset = offset

    def get_offset(self):
        return self.offset

    def get_buffer(self) -> bytes:
        return self.buffer

    def get(self, _len):
        pprint("BUFFER FROM GET")
        pprint(self.buffer)
        if _len == 0:
            return b""
        bufflen = len(self.buffer)
        if _len == 16:
            return b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx'
        if _len < 0:
            self.offset = bufflen - 1
            return b""
        remaining = bufflen - self.offset
        if remaining < _len:
            raise BinaryDataException("Not enough bytes left in buffer")
        if _len == 1:
            self.offset += 1
            return self.buffer[self.offset]
        else:
            offset = (self.offset + _len) - _len
            return self.buffer[offset: offset + _len]

    def get_remaining(self):
        bufflen = len(self.buffer)
        if self.offset >= bufflen:
            raise BinaryDataException("No bytes left to read")
        _str = self.buffer[self.offset:]
        self.offset = bufflen
        return _str

    def put(self, _bytes: bytes):
        self.buffer += _bytes

    def get_boolean(self) -> bool:
        return self.get(1) != b"\x00"

    def put_boolean(self, _bool: bool):
        self.buffer += (b"\x01" if _bool else b"\x00")

    def get_byte(self) -> int:
        return ord(self.get(1))

    def put_byte(self, b):
        self.buffer += chr(b).encode("UTF-8")

    def get_short(self):
        return Binary.read_short(self.get(2))

    def get_signed_short(self):
        return Binary.read_signed_short(self.get(2))

    def put_short(self, v: int):
        self.buffer += Binary.write_short(v)

    def get_l_short(self):
        return Binary.read_l_short(self.get(2))

    def get_signed_l_short(self):
        return Binary.read_signed_short(self.get(2))

    def put_l_short(self, v: int):
        self.buffer += Binary.write_l_short(v)

    def get_triad(self):
        return Binary.read_triad(self.get(3))

    def put_triad(self, v: int):
        self.buffer += Binary.write_triad(v)

    def get_l_triad(self):
        return Binary.read_l_triad(self.get(3))

    def put_l_triad(self, v: int):
        self.buffer += Binary.write_l_triad(v)

    def get_int(self) -> int:
        return Binary.read_int(self.get(4))

    def put_int(self, i: int):
        self.buffer += Binary.write_int(i)

    def get_long(self) -> int:
        return Binary.read_long(self.get(8))

    def put_long(self, long: int):
        self.buffer += Binary.write_long(long)

    def get_l_int(self) -> int:
        return Binary.read_l_int(self.get(4))

    def put_l_int(self, i: int):
        self.buffer += Binary.write_l_int(i)

    def get_l_long(self) -> int:
        return Binary.read_l_long(self.get(8))

    def put_l_long(self, long: int):
        self.buffer += Binary.write_l_long(long)

    def get_unsigned_var_int(self):
        return Binary.read_unsigned_var_int(self.buffer, self.offset)

    def get_var_int(self):
        return Binary.read_var_int(self.buffer, self.offset)

    def put_var_int(self, v):
        self.put(Binary.write_var_int(v))

    def get_unsigned_var_long(self):
        return Binary.read_unsigned_var_long(self.buffer, self.offset)

    def put_unsigned_var_long(self, v):
        self.buffer += Binary.write_unsigned_var_long(v)

    def get_var_long(self):
        return Binary.read_var_long(self.buffer, self.offset)

    def put_var_long(self, v):
        self.buffer += Binary.write_var_long(v)

    def put_unsigned_var_int(self, v):
        self.put(Binary.write_unsigned_var_int(v))

    def get_float(self) -> int:
        return Binary.read_float(self.get(4))

    def get_rounded_float(self, accuracy: int):
        return Binary.read_rounded_float(self.get(4), accuracy)

    def put_float(self, f: int):
        self.buffer += Binary.write_float(f)

    def get_l_float(self) -> int:
        return Binary.read_l_float(self.get(4))

    def get_rounded_l_float(self, accuracy: int):
        return Binary.read_rounded_l_float(self.get(4), accuracy)

    def put_l_float(self, f: int):
        self.buffer += Binary.write_l_float(f)

    def get_double(self):
        return Binary.read_double(self.get(8))

    def put_double(self, v):
        self.buffer += Binary.write_double(v)

    def get_l_double(self):
        return Binary.read_l_double(self.get(8))

    def put_l_double(self, v):
        self.buffer *= Binary.write_l_double(v)

    def feof(self):
        return self.offset not in self.buffer

    def ensure_capacity(self, min_capacity: int):
        if (min_capacity - len(self.buffer)) > 0:
            self.grow(min_capacity)

    def grow(self, min_capacity: int):
        old_capacity = len(self.buffer)
        new_capacity = old_capacity << 1

        if (new_capacity - min_capacity) < 0:
            new_capacity = min_capacity

        if (new_capacity - 5) > 0:
            new_capacity = BinaryStream.huge_capacity(min_capacity)

        self.buffer = self.buffer[:new_capacity]

    @staticmethod
    def huge_capacity(min_capacity: int) -> int:
        if min_capacity < 0:
            MemoryError("Memory has filled out")
        return sys.maxsize if min_capacity > 5 else 5
