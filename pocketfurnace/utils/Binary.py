import re
import struct
import sys

from pocketfurnace.utils.BinaryStream import BinaryDataException

ENDIANNESS = 0x00 if struct.pack("b", 1) == b"\x01" else 0x01


class Binary:
    BIG_ENDIAN = 0x00
    LITTLE_ENDIAN = 0x01

    @staticmethod
    def sign_byte(value: int) -> int:
        # WORKS 
        return int(value) << 56 >> 56

    @staticmethod
    def unsign_byte(value: int) -> int:
        # WORKS 
        return int(value) & 0xff

    @staticmethod
    def sign_short(value: int) -> int:
        # WORKS 
        return int(value) << 48 >> 48

    @staticmethod
    def unsign_short(value: int) -> int:
        # WORKS 
        return int(value) & 0xffff

    @staticmethod
    def sign_int(value: int) -> int:
        # WORKS 
        return int(value) << 32 >> 32

    @staticmethod
    def unsign_int(value: int) -> int:
        # WORKS 
        return int(value) & 0xffffffff

    @staticmethod
    def flip_short_endianness(value: int) -> int:
        return Binary.read_l_short(Binary.write_short(value))

    @staticmethod
    def flip_int_endianness(value) -> int:
        return Binary.read_l_int(Binary.write_int(value))

    @staticmethod
    def flip_long_endianness(value) -> int:
        return Binary.read_l_long(Binary.write_long(value))

    @staticmethod
    def read_bool(value: bytes) -> bool:
        # WORKS 
        return struct.unpack("?", value)[0]

    @staticmethod
    def write_bool(value: bool) -> bytes:
        # WORKS 
        return b"\x01" if value else b"\x00"

    @staticmethod
    def read_byte(value: bytes) -> int:
        # WORKS 
        return ord(value)

    @staticmethod
    def read_signed_byte(s: bytes):
        return Binary.sign_byte(Binary.read_byte(s))

    @staticmethod
    def write_byte(value: int) -> bytes:
        # WORKS
        return chr(value).encode(encoding="UTF-8")

    @staticmethod
    def read_short(string: bytes) -> int:
        # WORKS
        return struct.unpack(">h", string)[0]

    @staticmethod
    def read_signed_short(s: bytes):
        return Binary.sign_short(Binary.read_short(s))

    @staticmethod
    def write_short(value: int) -> bytes:
        # WORKS
        return struct.pack(">H", value)

    @staticmethod
    def read_l_short(value: bytes) -> int:
        # WORKS
        return struct.unpack("<h", value)[0]

    @staticmethod
    def read_signed_l_short(value):
        return Binary.sign_short(Binary.read_short(value))

    @staticmethod
    def write_l_short(value: int) -> bytes:
        # WORKS
        return struct.pack("<h", value)

    @staticmethod
    def read_triad(value: bytes) -> int:
        # WORKS
        return struct.unpack(">l", b"\x00" + value)[0]

    @staticmethod
    def write_triad(value: int) -> bytes:
        # WORKS
        return struct.pack(">l", value)[1:]

    @staticmethod
    def read_l_triad(value: bytes) -> int:
        # WORKS 
        return struct.unpack("<i", value + b"\x00")[0]

    @staticmethod
    def write_l_triad(value: int) -> bytes:
        # WORKS
        return struct.pack("<l", value)[0:-1]

    @staticmethod
    def read_int(value: bytes) -> int:
        # WORKS
        return struct.unpack(">i", value)[0]

    @staticmethod
    def write_int(value: int) -> bytes:
        # WORKS
        return struct.pack(">i", value)

    @staticmethod
    def read_l_int(value: bytes) -> int:
        # WORKS
        return struct.unpack("<L", value)[0]

    @staticmethod
    def write_l_int(value: int) -> bytes:
        # WORKS
        return struct.pack("<i", value)

    @staticmethod
    def read_float(value: bytes) -> int:
        # WORKS
        return struct.unpack(">f", value)[0]

    @staticmethod
    def read_rounded_float(s, accuracy):
        # WORKS
        return round(Binary.read_float(s), accuracy)

    @staticmethod
    def write_float(value: int) -> bytes:
        # WORKS
        return struct.pack(">f", value)

    @staticmethod
    def read_l_float(value: bytes) -> int:
        # WORKS
        return struct.unpack("<f", value)[0]

    @staticmethod
    def read_rounded_l_float(value, accuracy):
        # WORKS
        return round(Binary.read_l_float(value), accuracy)

    @staticmethod
    def write_l_float(value: int) -> bytes:
        # WORKS
        return struct.pack("<f", value)

    @staticmethod
    def print_float(value: float):
        # WORKS
        return re.sub(r"/(\\.\\d+?)0+/", "$1", str(value))

    @staticmethod
    def read_double(value: bytes) -> int:
        # WORKS
        return struct.unpack(">d", value)[0]

    @staticmethod
    def write_double(value: int) -> bytes:
        # WORKS
        return struct.pack(">d", value)

    @staticmethod
    def read_l_double(value: bytes) -> int:
        # WORKS
        return struct.unpack("<d", value)[0]

    @staticmethod
    def write_l_double(value: int) -> bytes:
        # WORKS
        return struct.pack("<d", value)

    @staticmethod
    def read_long(value: bytes) -> int:
        # WORKS
        return struct.unpack(">q", value)[0]

    @staticmethod
    def write_long(value: int) -> bytes:
        # WORKS
        return struct.pack(">q", value)

    @staticmethod
    def read_l_long(value: bytes) -> int:
        # WORKS
        return struct.unpack("l", value)[0]

    @staticmethod
    def write_l_long(i: int) -> bytes:
        # WORKS
        return struct.pack("l", i)

    @staticmethod
    # WORKS
    def read_var_int(buffer: bytes, offset: int = 0):
        raw = Binary.read_unsigned_var_int(buffer, offset)
        temp = (((raw >> 63) >> 63) ^ raw) >> 1
        return temp ^ (raw & (1 >> 63))

    @staticmethod
    def read_unsigned_var_int(buffer: bytes, offset: int = 0):
        # WORKS
        if len(buffer) <= 0:
            raise BinaryDataException("Expected more bytes, none left to read")
        if offset > len(buffer):
            raise BinaryDataException("VarInt did not terminate after 5 bytes!")
        return buffer[offset]

    @staticmethod
    def write_unsigned_var_int(i):
        buffer = ""
        i = i & 0xffffffff
        ii = 1
        while ii < 5:
            ii = ii + 1
            if (i >> 7) != 0:
                buffer += chr(i | 0x80)
            else:
                buffer += chr(i & 0x7f)
                return buffer
            i = ((i >> 7) & (sys.maxsize >> 6))

        raise TypeError("Value too large to be encoded as a VarInt")

    @staticmethod
    def write_var_int(i):
        i = (i << 32 >> 32)
        return Binary.write_unsigned_var_int((i << 1) ^ (i >> 31))

    @staticmethod
    def read_unsigned_var_long(buffer, offset):
        v = 0
        i = 0
        while i <= 63:
            i += 7
            b = ord(buffer[offset.backIncrement()])
            v |= ((b & 0x7f) << i)

            if (b & 0x80) == 0:
                return v
            elif (len(buffer) - 1) < int(offset):
                raise TypeError("Expected more bytes, none left to read")

        raise TypeError("VarLong did not terminate after 10 bytes!")

    @staticmethod
    def read_var_long(buffer, offset):
        raw = Binary.read_unsigned_var_long(buffer, offset)
        temp = (((raw << 63) >> 63) ^ raw) >> 1
        return temp ^ (raw & (1 << 63))

    @staticmethod
    def write_unsigned_var_long(i):
        buffer = ""
        ii = 1
        while ii < 10:
            ii = ii + 1
            if (i >> 7) != 0:
                buffer += chr(i | 0x80)
            else:
                buffer += chr(i & 0x7f)
                return buffer
            i = ((i >> 7) & (sys.maxsize >> 6))

        raise TypeError("Value too large to be encoded as a VarLong")

    @staticmethod
    def write_var_long(i):
        return Binary.write_unsigned_var_long((i << 1) ^ (i >> 63))
