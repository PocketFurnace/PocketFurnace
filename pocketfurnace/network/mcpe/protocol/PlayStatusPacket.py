from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo


class PlayStatusPacket(DataPacket):
    NID = ProtocolInfo.PLAY_STATUS_PACKET

    LOGIN_SUCCESS = 0
    LOGIN_FAILED_CLIENT = 1
    LOGIN_FAILED_SERVER = 2
    PLAYER_SPAWN = 3
    LOGIN_FAILED_INVALID_TENANT = 4
    LOGIN_FAILED_VANILLA_EDU = 5
    LOGIN_FAILED_EDU_VANILLA = 6
    LOGIN_FAILED_SERVER_FULL = 7

    status = None

    def decode_payload(self):
        self.status = self.get_int()

    def can_be_sent_before_login(self):
        return True

    def encode_payload(self):
        self.put_int(self.status)
