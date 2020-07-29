from pocketfurnace.utils.BinaryStream import BinaryStream
from pocketfurnace.utils.UUID import UUID


class NetworkBinaryStream(BinaryStream):
    def get_string(self):
        self.get(self.get_unsigned_var_int())

    def put_string(self, value):
        self.put_unsigned_var_int(len(value))
        self.buffer += value

    def get_uuid(self):
        part1 = self.get_l_int()
        part0 = self.get_l_int()
        part3 = self.get_l_int()
        part2 = self.get_l_int()
        return UUID(part0, part1, part2, part3)

    def put_uuid(self, uuid: UUID):
        self.put_l_int(uuid.get_part(1))
        self.put_l_int(uuid.get_part(0))
        self.put_l_int(uuid.get_part(3))
        self.put_l_int(uuid.get_part(2))