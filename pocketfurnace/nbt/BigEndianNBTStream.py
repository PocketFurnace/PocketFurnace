from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.utils.Binary import Binary
import struct


class BigEndianNBTStream(NBTStream):
    def get_short(self) -> int:
        return Binary.read_short(self.get(2))

    def get_signed_short(self) -> int:
        return Binary.read_signed_short(self.get(2))

    def put_short(self, v: int):
        self.buffer += Binary.write_short(v)

    def get_int(self) -> int:
        return Binary.read_int(self.get(4))

    def put_int(self, v: int):
        self.buffer += Binary.write_int(v)

    def get_long(self) -> int:
        return Binary.read_long(self.get(8))

    def put_long(self, v: int):
        self.buffer += Binary.write_long(v)

    def get_float(self) -> float:
        return Binary.read_float(self.get(4))

    def put_float(self, v: float):
        self.buffer += Binary.write_float(v)

    def get_double(self) -> float:
        return Binary.read_double(self.get(8))

    def put_double(self, v: float):
        self.buffer += Binary.write_double(v)

    def get_int_array(self):
        length = self.get_int()
        return struct.unpack("N*", self.get(length * 4))  # need check

    def put_int_array(self, array):
        self.put_int(len(array))
        self.put(struct.pack("N*", array))  # need check
