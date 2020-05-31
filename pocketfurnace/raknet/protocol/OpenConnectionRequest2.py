from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.OfflineMessage import OfflineMessage


class OpenConnectionRequest2(OfflineMessage):
    ID = MessageIdentifiers.ID_OPEN_CONNECTION_REQUEST_2

    client_id = None
    server_address = None
    mtu_size = None

    def _encodePayload(self):
        self._write_magic()
        self.put_address(self.server_address)
        self.put_short(self.mtu_size)
        self.put_long(self.client_id)

    def _decodePayload(self):
        self._read_magic()
        self.server_address = self.get_address()
        self.mtu_size = self.get_short()
        self.client_id = self.get_long()
