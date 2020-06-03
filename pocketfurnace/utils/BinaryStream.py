from .Binary import Binary


class BinaryStream:
    offset = 0
    buffer = b""

    def __init__(self, buffer: bytes = b"", offset: int = 0):
        self.buffer = buffer
        self.offset = offset

    def reset(self):
        self.buffer = b""
        self.offset = 0

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

    def get(self, length):
        if length < 0:
            return b""
        elif isinstance(length, bool) and length:
            return self.buffer[0:self.offset]
        else:
            buffer = self.buffer[self.offset:self.offset+length]
            self.offset += length
            return buffer

    def get_remaining(self):
        bufflen = len(self.buffer)
        if self.offset >= bufflen:
            raise ValueError("No bytes left to read")
        string = self.buffer[self.offset:]
        self.offset = bufflen
        return string

    def put(self, _bytes: bytes):
        self.buffer += _bytes

    def get_bool(self) -> bool:
        return self.get(1) != b"\x00"

    def put_bool(self, _bool: bool):
        self.buffer += (b"\x01" if _bool else b"\x00")

    def get_byte(self) -> int:
        return ord(self.get(1))

    def put_byte(self, b: int):
        self.buffer += chr(b).encode("UTF-8")

    def get_short(self) -> int:
        return Binary.read_short(self.get(2))

    def get_signed_short(self):
        return Binary.read_signed_short(self.get(2))

    def put_short(self, v: int):
        self.buffer += Binary.write_short(v)

    def get_l_short(self) -> int:
        return Binary.read_l_short(self.get(2))

    def get_signed_l_short(self) -> int:
        return Binary.read_signed_short(self.get(2))

    def put_l_short(self, v: int):
        self.buffer += Binary.write_l_short(v)

    def get_triad(self) -> int:
        return Binary.read_triad(self.get(3))

    def put_triad(self, v: int):
        self.buffer += Binary.write_triad(v)

    def get_l_triad(self) -> int:
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

    def get_unsigned_var_int(self) -> int:
        return Binary.read_unsigned_var_int(self.buffer, self.offset)

    def get_var_int(self) -> int:
        return Binary.read_var_int(self.buffer, self.offset)

    def put_var_int(self, v: int):
        self.put(Binary.write_var_int(v))

    def get_unsigned_var_long(self) -> int:
        return Binary.read_unsigned_var_long(self.buffer, self.offset)

    def put_unsigned_var_long(self, v: int):
        self.buffer += Binary.write_unsigned_var_long(v)

    def get_var_long(self) -> int:
        return Binary.read_var_long(self.buffer, self.offset)

    def put_var_long(self, v: int):
        self.buffer += Binary.write_var_long(v)

    def put_unsigned_var_int(self, v: int):
        self.put(Binary.write_unsigned_var_int(v))

    def get_float(self) -> float:
        return Binary.read_float(self.get(4))

    def get_rounded_float(self, accuracy: int) -> float:
        return Binary.read_rounded_float(self.get(4), accuracy)

    def put_float(self, f: float):
        self.buffer += Binary.write_float(f)

    def get_l_float(self) -> float:
        return Binary.read_l_float(self.get(4))

    def get_rounded_l_float(self, accuracy: int):
        return Binary.read_rounded_l_float(self.get(4), accuracy)

    def put_l_float(self, f: float):
        self.buffer += Binary.write_l_float(f)

    def get_double(self) -> float:
        return Binary.read_double(self.get(8))

    def put_double(self, v: float):
        self.buffer += Binary.write_double(v)

    def get_l_double(self):
        return Binary.read_l_double(self.get(8))

    def put_l_double(self, v: float):
        self.buffer *= Binary.write_l_double(v)

    # noinspection PyStatementEffect
    def feof(self) -> bool:
        try:
            self.buffer[self.offset]
            return True
        except(NameError, KeyError, IndexError):
            return False
