from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.protocol import EncapsulatedPacket
from pocketfurnace.raknet.server import PyRakLibServer, ServerInstance
from pocketfurnace.utils.Binary import Binary


class ServerHandler:
    server = None
    instance = None

    def __init__(self, server: PyRakLibServer, instance: ServerInstance):
        self.server = server
        self.instance = instance

    def send_encapsulated(self, identifier: str, packet: EncapsulatedPacket, flags: int = PyRakLib.PRIORITY_NORMAL):
        buffer = ""
        buffer += chr(PyRakLib.PACKET_ENCAPSULATED)
        buffer += chr(len(identifier))
        buffer += identifier
        buffer += chr(flags)
        buffer += packet.to_internal_binary()
        self.server.push_main_to_thread_packet(buffer)

    def send_raw(self, address: str, port: int, payload: bytes):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_RAW)
        buffer += chr(len(address))
        buffer += address
        buffer += Binary.write_short(port)
        buffer += payload
        self.server.push_main_to_thread_packet(buffer)

    def close_session(self, identifier: str, reason: str):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_CLOSE_SESSION)
        buffer += chr(len(identifier))
        buffer += identifier
        buffer += chr(len(reason))
        buffer += reason
        self.server.push_main_to_thread_packet(buffer)

    def send_option(self, name: str, value: str):
        buffer = chr(PyRakLib.PACKET_SET_OPTION)
        buffer += chr(len(name))
        buffer += name
        buffer += value
        self.server.push_main_to_thread_packet(buffer)

    def block_address(self, address: str, timeout: int):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_BLOCK_ADDRESS)
        buffer += chr(len(address))
        buffer += address
        buffer += Binary.write_int(timeout)
        self.server.push_main_to_thread_packet(buffer)

    def unblock_address(self, address: str):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_UNBLOCK_ADDRESS)
        buffer += chr(len(address))
        buffer += address
        self.server.push_main_to_thread_packet(buffer)

    def shutdown(self):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_SHUTDOWN)
        self.server.push_main_to_thread_packet(buffer)
        self.server.shutdown()
        self.server.join()
        # time.sleep(50000 / 1000000.0)  # Sleep for 1 tick

    def emergency_shutdown(self):
        self.server.shutdown()
        self.server.push_main_to_thread_packet(chr(PyRakLib.PACKET_EMERGENCY_SHUTDOWN))  # Emergency Shutdown

    def invalid_session(self, identifier):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_INVALID_SESSION)
        buffer += chr(len(identifier))
        buffer += identifier
        self.server.push_main_to_thread_packet(buffer)

    def handle_packet(self):
        packet = self.server.read_thread_to_main_packet()
        if packet is None:
            return
        packet_id = ord(packet[0])
        offset = 1
        if packet_id == PyRakLib.PACKET_ENCAPSULATED:
            offset += 1
            length = ord(packet[offset])
            identifier = packet[offset:length]
            offset += length
            flags = ord(packet[offset])
            buffer = packet[offset]
            self.instance.handle_encapsulated(identifier, EncapsulatedPacket.from_internal_binary(buffer), flags)
        elif packet_id == PyRakLib.PACKET_RAW:
            length = ord(packet[offset + 1])
            address = packet[offset:length]
            offset += length
            port = Binary.read_short(packet[offset:2])
            offset += 2
            payload = packet[offset:]
            self.instance.handle_raw(address, port, payload)
        elif packet_id == PyRakLib.PACKET_SET_OPTION:
            length = ord(packet[offset + 1])
            name = packet[offset:length]
            offset += length
            value = packet[offset:]
            self.instance.handle_option(name, value)
        elif packet_id == PyRakLib.PACKET_OPEN_SESSION:
            length = ord(packet[offset + 1])
            identifier = packet[offset:length]
            offset += length
            length = ord(packet[offset + 1])
            address = packet[offset:length]
            offset += length
            port = Binary.read_short(packet[offset:2])
            offset += 2
            client_id = Binary.read_long(packet[offset:8])
            self.instance.open_session(identifier, address, port, client_id)
        elif packet_id == PyRakLib.PACKET_CLOSE_SESSION:
            length = ord(packet[offset + 1])
            identifier = packet[offset:length]
            offset += length
            length = ord(packet[offset + 1])
            reason = packet[offset:length]
            self.instance.close_session(identifier, reason)
        elif packet_id == PyRakLib.PACKET_INVALID_SESSION:
            length = ord(packet[offset + 1])
            identifier = packet[offset:length]
            self.instance.close_session(identifier, "Invalid session")
        elif packet_id == PyRakLib.PACKET_ACK_NOTIFICATION:
            length = ord(packet[offset + 1])
            identifier = packet[offset:length]
            offset += length
            identifier_ack = Binary.read_int(packet[offset:4])
            self.instance.notify_ack(identifier, identifier_ack)
        elif packet_id == PyRakLib.PACKET_REPORT_PING:
            length = ord(packet[offset + 1])
            identifier = packet[offset:length]
            offset += length
            ping_ms = Binary.read_int(packet[offset:4])
            self.instance.update_ping(identifier, ping_ms)
        return False
