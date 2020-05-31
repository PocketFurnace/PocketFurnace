import struct
import sys
import re
from pprint import pprint

# ENDIANNESS = Binary.BIG_ENDIAN if struct.pack("d", 1) == "\77\360\0\0\0\0\0\0" else Binary.LITTLE_ENDIAN

class Binary:
    BIG_ENDIAN = 0x00
    LITTLE_ENDIAN = 0x01

    @staticmethod
    def sign_byte(value: int):
        return int(value) << 56 >> 56

    @staticmethod
    def unsign_byte(value: int):
        return int(value) & 0xff

    @staticmethod
    def sign_short(value: int):
        return int(value) << 48 >> 48

    @staticmethod
    def unsign_short(value: int):
        return int(value) & 0xffff

    @staticmethod
    def sign_int(value: int):
        return int(value) << 32 >> 32

    @staticmethod
    def unsign_int(value: int):
        return int(value) & 0xffffffff

    @staticmethod
    def read_bool(b: bytes) -> bool:
        return struct.unpack("?", b)[0]

    @staticmethod
    def write_bool(b: bool) -> bytes:
        return b"\x01" if b else b"\x00"

    @staticmethod
    def read_byte(s: bytes) -> int:
        return ord(s)

    @staticmethod
    def read_signed_byte(s: str):
        return Binary.sign_byte(Binary.read_byte(s))

    @staticmethod
    def write_byte(i: int) -> bytes:
        return chr(i).encode()

    @staticmethod
    def read_short(string: bytes) -> int:
        print("ENTRADA DE SHORT:")
        pprint(string)
        return struct.unpack(">h", string)[0]

    @staticmethod
    def read_signed_short(s: bytes):
        return Binary.sign_short(Binary.read_short(s))

    @staticmethod
    def write_short(i: int) -> bytes:
        return struct.pack(">h", i)

    @staticmethod
    def read_l_short(string: bytes) -> int:
        return struct.unpack("<h", string)[0]

    @staticmethod
    def read_signed_l_short(s):
        return Binary.sign_short(Binary.read_short(s))

    @staticmethod
    def write_l_short(i: int) -> bytes:
        return struct.pack("<h", i)

    @staticmethod
    def read_triad(s: bytes) -> int:
        return struct.unpack(">l", b"".join([b"\x00", s[0], s[1], s[2]]))[0]

    @staticmethod
    def write_triad(i: int) -> bytes:
        return struct.pack(">l", i)[1:]

    @staticmethod
    def read_l_triad(s: bytes) -> int:
        return struct.unpack("<l", b"".join([s[0], s[1], s[2], b"\x00"]))[0]

    @staticmethod
    def write_l_triad(i: int) -> bytes:
        return struct.pack("<l", i)[0:-1]

    @staticmethod
    def read_int(s: bytes) -> int:
        return struct.unpack(">i", s)[0]

    @staticmethod
    def write_int(i: int) -> bytes:
        return struct.pack(">i", i)

    @staticmethod
    def read_l_int(s: bytes) -> int:
        return struct.unpack("V", s)[1]

    @staticmethod
    def write_l_int(i: int) -> bytes:
        return struct.pack("<i", i)

    @staticmethod
    def read_float(s: bytes) -> int:
        return struct.unpack(">f", s)[0]

    @staticmethod
    def read_rounded_float(s, accuracy):
        return round(Binary.read_float(s), accuracy)

    @staticmethod
    def write_float(f: int) -> bytes:
        return struct.pack(">f", f)

    @staticmethod
    def read_l_float(s: bytes) -> int:
        return struct.unpack("<f", s)[0]

    @staticmethod
    def read_rounded_l_float(s, accuracy):
        return round(Binary.read_l_float(s), accuracy)

    @staticmethod
    def write_l_float(f: int) -> bytes:
        return struct.pack("<f", f)

    @staticmethod
    def print_float(f):
        return re.match(r"/(\\.\\d+?)0+$/", "" + f).group(1)

    @staticmethod
    def read_double(s: bytes) -> int:
        return struct.unpack(">d", s)[0]

    @staticmethod
    def write_double(f: int) -> bytes:
        return struct.pack(">d", f)

    @staticmethod
    def read_l_double(s: bytes) -> int:
        return struct.unpack("<d", s)[0]

    @staticmethod
    def write_l_double(f: int) -> bytes:
        return struct.pack("<d", f)

    @staticmethod
    def read_long(s: bytes) -> int:
        return struct.unpack("l", s)[0]

    @staticmethod
    def write_long(i: int) -> bytes:
        return struct.pack("q", i)

    @staticmethod
    def read_l_long(s: bytes) -> int:
        return struct.unpack("<l", s)[0]

    @staticmethod
    def write_l_long(i: int) -> bytes:
        return struct.pack(">l", i)

    @staticmethod
    def read_unsigned_var_int(buffer, offset):
        v = 0
        i = 0
        while i <= 35:
            i += 7
            b = ord(buffer[offset.backIncrement()])
            v |= ((b & 0x7f) << i)

            if (b & 0x80) == 0:
                return v
            elif (len(buffer) - 1) < int(offset):
                raise TypeError("Expected more bytes, none left to read")
        raise TypeError("VarInt did not terminate after 5 bytes")

    @staticmethod
    def read_var_int(buffer, offset):
        raw = Binary.read_unsigned_var_int(buffer, offset)
        temp = (((raw << 63) >> 63) ^ raw) >> 1
        return temp ^ (raw & (1 << 63))

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

    @staticmethod
    def flip_short_endianness(i):
        return Binary.read_l_short(Binary.write_short(i))

    @staticmethod
    def flip_int_endianness(i):
        return Binary.read_l_int(Binary.write_int(i))

    @staticmethod
    def flip_long_endianness(i):
        return Binary.read_l_long(Binary.write_long(i))
