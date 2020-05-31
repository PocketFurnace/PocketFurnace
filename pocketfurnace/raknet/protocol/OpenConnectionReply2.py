from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.OfflineMessage import OfflineMessage


class OpenConnectionReply2(OfflineMessage):
    ID = MessageIdentifiers.ID_OPEN_CONNECTION_REPLY_2

    server_id = None
    client_address = None
    mtu_size = None
    server_security = False

    def _encodePayload(self):
        self._write_magic()
        self.put_long(self.server_id)
        self.put_address(self.client_address)
        self.put_short(self.mtu_size)
        self.put_byte(1 if self.server_security else 0)  # Server security

    def _decodePayload(self):
        self._read_magic()
        self.server_id = self.get_long()
        self.client_address = self.get_address()
        self.mtu_size = self.get_short()
        self.server_security = self.get_byte() != 0  # Server security
