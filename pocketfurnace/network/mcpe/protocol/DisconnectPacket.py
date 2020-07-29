from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo


class DisconnectPacket(DataPacket):
    NID = ProtocolInfo.DISCONNECT_PACKET

    hideDisconnectionScreen = False
    message = ""

    def can_be_sent_before_login(self):
        return True

    def decode_payload(self):
        self.hideDisconnectionScreen = self.get_bool()
        if not self.hideDisconnectionScreen:
            self.message = self.get_string()

    def encode_payload(self):
        self.put_bool(self.hideDisconnectionScreen)
        if not self.hideDisconnectionScreen:
            self.put_string(self.message)