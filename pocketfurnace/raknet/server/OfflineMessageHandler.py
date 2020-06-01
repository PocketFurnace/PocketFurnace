from pocketfurnace.raknet.protocol.IncompatibleProtocolVersion import IncompatibleProtocolVersion
from pocketfurnace.raknet.protocol.OpenConnectionReply1 import OpenConnectionReply1
from pocketfurnace.raknet.protocol.OpenConnectionReply2 import OpenConnectionReply2
from pocketfurnace.raknet.protocol.OpenConnectionRequest1 import OpenConnectionRequest1
from pocketfurnace.raknet.protocol.OpenConnectionRequest2 import OpenConnectionRequest2
from pocketfurnace.raknet.protocol.UnconnectedPing import UnconnectedPing
from pocketfurnace.raknet.protocol.UnconnectedPong import UnconnectedPong
from pocketfurnace.raknet.server.Session import Session
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress
from pprint import pprint


class OfflineMessageHandler:
    session_manager = None

    def __init__(self, session_manager):
        self.session_manager = session_manager

    def handle(self, packet, address: InternetAddress) -> bool:
        if packet.ID == UnconnectedPing.ID:
            pk = UnconnectedPong()
            pk.server_id = self.session_manager.get_id()
            pk.ping_id = packet.ping_id
            pk.server_name = self.session_manager.get_name()
            self.session_manager.send_packet(pk, address)
            return True
        if packet.ID == OpenConnectionRequest1.ID:
            server_protocol = self.session_manager.get_protocol_version()
            if packet.protocol_version != server_protocol:
                pk = IncompatibleProtocolVersion()
                pk.protocol_version = server_protocol
                pk.server_id = self.session_manager.get_id()
                self.session_manager.send_packet(pk, address)
            else:
                pk = OpenConnectionReply1()
                pk.mtu_size = packet.mtu_size + 28
                pk.server_id = self.session_manager.get_id()
                self.session_manager.send_packet(pk, address)
                return True
        if packet.ID == OpenConnectionRequest2.ID:
            if packet.server_address.port == self.session_manager.get_port() or not self.session_manager.port_checking:
                if packet.mtu_size < Session.MIN_MTU_SIZE:
                    print("bad mtu size")
                    return True
                mtu_size = min(packet.mtu_size, self.session_manager.get_max_mtu_size())
                pk = OpenConnectionReply2()
                pk.mtu_size = mtu_size
                pk.server_id = self.session_manager.get_id()
                pk.client_address = address
                self.session_manager.send_packet(pk, address)
                self.session_manager.create_session(address, packet.client_id, mtu_size)
            else:
                print("Not creating session due to mismatched port")
            return True
        return False
