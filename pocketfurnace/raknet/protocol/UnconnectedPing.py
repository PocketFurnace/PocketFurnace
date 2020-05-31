from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.OfflineMessage import OfflineMessage


class UnconnectedPing(OfflineMessage):

    ID = MessageIdentifiers.ID_UNCONNECTED_PING
    ping_id = None

    def _encodePayload(self):
        self.put_long(self.ping_id)
        self._write_magic()

    def _decodePayload(self):
        self.ping_id = self.get_long()
        self._read_magic()
