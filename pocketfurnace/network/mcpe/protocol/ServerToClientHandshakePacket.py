from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo


class ServerToClientHandshakePacket(DataPacket):
    NID = ProtocolInfo.SERVER_TO_CLIENT_HANDSHAKE_PACKET

    jwt = None

    def can_be_sent_before_login(self):
        return True

    def decode_payload(self):
        self.jwt = self.get_string()

    def encode_payload(self):
        self.put_string(self.jwt)
