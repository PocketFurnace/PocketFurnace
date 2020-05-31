from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.Packet import Packet


class ConnectionRequest(Packet):
    ID = MessageIdentifiers.ID_CONNECTION_REQUEST
    client_id = None
    send_ping_time = None
    use_security = False

    def _encodePayload(self):
        self.put_long(self.client_id)
        self.put_long(self.send_ping_time)
        self.put_byte(1 if self.use_security else 0)

    def _decodePayload(self):
        self.client_id = self.get_long()
        self.send_ping_time = self.get_long()
        self.use_security = self.get_byte() != 0
