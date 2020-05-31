from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.OfflineMessage import OfflineMessage


class IncompatibleProtocolVersion(OfflineMessage):
    ID = MessageIdentifiers.ID_INCOMPATIBLE_PROTOCOL_VERSION
    protocol_version = None
    server_id = None

    def _encodePayload(self):
        self.put_byte(self.protocol_version)
        self._write_magic()
        self.put_long(self.server_id)

    def _decodePayload(self):
        self.protocol_version = self.get_byte()
        self._read_magic()
        self.server_id = self.get_long()
