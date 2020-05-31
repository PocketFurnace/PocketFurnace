from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.Packet import Packet


class DisconnectNotification(Packet):

    ID = MessageIdentifiers.ID_DISCONNECTION_NOTIFICATION

    def _encodePayload(self) -> None:
        pass

    def _decodePayload(self) -> None:
        pass
