from pocketfurnace.nbt.LittleEndianNBTStream import LittleEndianNBTStream
from pocketfurnace.utils.Binary import Binary


class NetworkLittleEndianNBTStream(LittleEndianNBTStream):
    def get_int(self) -> int:
        return Binary.read_var_int(self.buffer, self.offset)

    def put_int(self, v: int):
        self.put(Binary.write_var_int(v))

    def get_long(self) -> int:
        return Binary.read_var_long(self.buffer, self.offset)

    def put_long(self, v: int):
        self.put(Binary.write_var_long(v))

    def get_string(self) -> bytes:
        return self.get(self.check_read_string_length(Binary.read_unsigned_var_int(self.buffer, self.offset)))

    def put_string(self, v: str):
        self.put(Binary.write_unsigned_var_int(self.check_write_string_length(len(v))) + bytes(v))

    def get_int_array(self):
        length = self.get_int()
        ret = []
        for i in range(0, length):
            ret.append(self.get_int())
        return ret

    def put_int_array(self, array):
        self.put_int(len(array))
        for v in array:
            self.put_int(v)
