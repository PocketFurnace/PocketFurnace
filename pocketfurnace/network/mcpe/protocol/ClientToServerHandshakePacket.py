from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo


class ClientToServerHandshakePacket(DataPacket):
    NID = ProtocolInfo.CLIENT_TO_SERVER_HANDSHAKE_PACKET

    def can_be_sent_before_login(self):
        return True

    def encode_payload(self): pass

    def decode_payload(self): pass
