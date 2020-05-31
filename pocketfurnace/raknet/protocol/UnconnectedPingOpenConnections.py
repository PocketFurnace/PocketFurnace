
from pocketfurnace.raknet.protocol.UnconnectedPing import UnconnectedPing
from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers


class UnconnectedPingOpenConnections(UnconnectedPing):
    ID = MessageIdentifiers.ID_UNCONNECTED_PING_OPEN_CONNECTIONS
