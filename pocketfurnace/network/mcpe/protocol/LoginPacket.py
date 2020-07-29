import json

from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo
from pocketfurnace.utils.Utils import Utils


class LoginPacket(DataPacket):
    NID = ProtocolInfo.LOGIN_PACKET

    username = None
    protocol = None
    clientUUID = None
    clientId = None
    xuid = None
    identityPublicKey = None
    serverAddress = None
    locale = None
    chainData = {}
    clientDataJwt = None
    clientData = {}
    skipVerification = False

    def can_be_sent_before_login(self):
        return True

    def may_have_unread_bytes(self):
        return self.protocol != None and self.protocol != ProtocolInfo.MCBE_PROTOCOL_VERSION

    def decode_payload(self):
        self.protocol = self.get_int()
        try:
            buffer = DataPacket.NetworkBinaryStream(self.get_string())
            self.chainData = json.loads(buffer.get(buffer.getLInt()))
            hasExtraData = False
            for chain in self.chainData["chain"]:
                webtoken = Utils.decode_jwt(chain)
                if webtoken["extraData"] in locals() or webtoken["extraData"] in globals():
                    if hasExtraData:
                        raise Exception("Found 'extraData' multiple times in key chain")
                    hasExtraData = True
                    if webtoken["extraData"]["displayName"] in locals() or webtoken["extraData"][
                        "displayName"] in globals():
                        self.username = webtoken["extraData"]["displayName"]
                    if webtoken["extraData"]["identity"] in locals() or webtoken["extraData"]["identity"] in globals():
                        self.clientUUID = webtoken["extraData"]["identity"]
                    if webtoken["extraData"]["XUID"] in locals() or webtoken["extraData"]["XUID"] in globals():
                        self.xuid = webtoken["extraData"]["XUID"]
                if webtoken["identityPublicKey"] in locals() or webtoken["identityPublicKey"] in globals():
                    self.identityPublicKey = webtoken["identityPublicKey"]
            self.clientDataJwt = buffer.get(buffer.getLInt())
            self.clientData = Utils.encode_jwt(self.clientDataJwt)
            self.clientId = self.clientData["ClientRandomId"] if self.clientData["ClientRandomId"] != None else None
            self.serverAddress = self.clientData["ServerAddress"] if self.clientData["ServerAddress"] != None else None
            self.locale = self.clientData["LanguageCode"] if self.clientData["LanguageCode"] != None else None
        except:
            if self.protocol == ProtocolInfo.MCBE_PROTOCOL_VERSION:
                raise Exception("Error")

    def encode_payload(self):
        pass
