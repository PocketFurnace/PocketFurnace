from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.Packet import Packet


class ConnectedPing(Packet):

    ID = MessageIdentifiers.ID_CONNECTED_PING
    send_ping_time = None

    def _encodePayload(self):
        self.put_long(self.send_ping_time)

    def _decodePayload(self):
        self.send_ping_time = self.get_long()
