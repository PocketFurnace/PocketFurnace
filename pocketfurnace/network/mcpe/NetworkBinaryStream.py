from pocketfurnace.utils.BinaryStream import BinaryStream


class NetworkBinaryStream(BinaryStream):
    DAMAGE_TAG = "Damage"
    DAMAGE_TAG_CONFLICT_RESOLUTION = "___Damage_ProtocolCollisionResolution___"

    def get_string(self) -> bytes:
        return self.get(self.get_unsigned_var_int())

    def put_string(self, v: str):
        self.put_unsigned_var_int(int(v))
