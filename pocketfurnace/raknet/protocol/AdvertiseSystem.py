from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.Packet import Packet


class AdvertiseSystem(Packet):
    ID = MessageIdentifiers.ID_ADVERTISE_SYSTEM
    server_name = None

    def _encodePayload(self):
        self.put_string(self.server_name)

    def _decodePayload(self):
        self.server_name = self.get_string()
