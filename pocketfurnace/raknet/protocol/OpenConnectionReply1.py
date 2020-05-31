from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.OfflineMessage import OfflineMessage


class OpenConnectionReply1(OfflineMessage):
    ID = MessageIdentifiers.ID_OPEN_CONNECTION_REPLY_1

    server_id = None
    server_security = False
    mtu_size = None

    def _encodePayload(self):
        self._write_magic()
        self.put_long(self.server_id)
        self.put_byte(1 if self.server_security else 0)  # Server security
        self.put_short(self.mtu_size)

    def _decodePayload(self):
        self._read_magic()
        self.server_id = self.get_long()
        self.server_security = self.get_byte() != 0  # Server security
        self.mtu_size = self.get_short()
