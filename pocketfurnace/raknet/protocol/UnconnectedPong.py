from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.OfflineMessage import OfflineMessage


class UnconnectedPong(OfflineMessage):
    ID = MessageIdentifiers.ID_UNCONNECTED_PONG

    ping_id = None
    server_id = None
    server_name = None

    def _encodePayload(self):
        self.put_long(self.ping_id)
        self.put_long(self.server_id)
        self._write_magic()
        self.put_string(self.server_name)

    def _decodePayload(self):
        self.ping_id = self.get_long()
        self.server_id = self.get_long()
        self._read_magic()
        self.server_name = self.get_string()
