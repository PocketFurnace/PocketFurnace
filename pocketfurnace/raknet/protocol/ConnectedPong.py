from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.Packet import Packet


class ConnectedPong(Packet):
    ID = MessageIdentifiers.ID_CONNECTED_PONG
    send_ping_time = None
    send_pong_time = None

    def _encodePayload(self):
        self.put_long(self.send_ping_time)
        self.put_long(self.send_pong_time)

    def _decodePayload(self):
        self.send_ping_time = self.get_long()
        self.send_pong_time = self.get_long()
