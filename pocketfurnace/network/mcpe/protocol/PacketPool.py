from pocketfurnace.network.mcpe.protocol.AdventureSettingsPacket import AdventureSettingsPacket
from pocketfurnace.network.mcpe.protocol.ClientToServerHandshakePacket import ClientToServerHandshakePacket
from pocketfurnace.network.mcpe.protocol.DisconnectPacket import DisconnectPacket
from pocketfurnace.network.mcpe.protocol.LoginPacket import LoginPacket
from pocketfurnace.network.mcpe.protocol.PlayStatusPacket import PlayStatusPacket
from pocketfurnace.network.mcpe.protocol.ResourcePacksInfoPacket import ResourcePacksInfoPacket
from pocketfurnace.network.mcpe.protocol.ServerToClientHandshakePacket import ServerToClientHandshakePacket


class PacketPool:
    packet_pool = {}

    def __init__(self):
        self.register_packets()

    def register_packet(self, packet):
        self.packet_pool[packet.NID] = packet.copy()

    def register_packets(self):
        self.register_packet(AdventureSettingsPacket)
        self.register_packet(ClientToServerHandshakePacket)
        self.register_packet(DisconnectPacket)
        self.register_packet(LoginPacket)
        self.register_packet(PlayStatusPacket)
        self.register_packet(ResourcePacksInfoPacket)
        self.register_packet(ServerToClientHandshakePacket)