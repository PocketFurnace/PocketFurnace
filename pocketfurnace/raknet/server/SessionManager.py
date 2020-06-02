import copy
import json
import math
import time
from pprint import pprint

from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.protocol.AdvertiseSystem import AdvertiseSystem
from pocketfurnace.raknet.protocol.EncapsulatedPacket import EncapsulatedPacket
from pocketfurnace.raknet.protocol.OpenConnectionReply1 import OpenConnectionReply1
from pocketfurnace.raknet.protocol.OpenConnectionReply2 import OpenConnectionReply2
from pocketfurnace.raknet.protocol.OpenConnectionRequest1 import OpenConnectionRequest1
from pocketfurnace.raknet.protocol.OpenConnectionRequest2 import OpenConnectionRequest2
from pocketfurnace.raknet.protocol.Packet import Packet
from pocketfurnace.raknet.protocol.UnconnectedPing import UnconnectedPing
from pocketfurnace.raknet.protocol.UnconnectedPingOpenConnections import UnconnectedPingOpenConnections
from pocketfurnace.raknet.protocol.UnconnectedPong import UnconnectedPong
from pocketfurnace.raknet.server.OfflineMessageHandler import OfflineMessageHandler
from pocketfurnace.raknet.server.Session import Session
from pocketfurnace.raknet.server.UDPServerSocket import UDPServerSocket
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress
from pocketfurnace.utils.Binary import Binary


def microtime(get_as_float=False):
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())


class SessionManager:
    RAKLIB_TPS = 100
    RAKLIB_TIME_PER_TICK = 1 / RAKLIB_TPS
    packet_pool = {}

    server = None
    socket = None

    receive_bytes = 0
    send_bytes = 0

    sessions = {}
    offline_message_handler = None

    name = ""

    packet_limit = 1000

    shutdown = False

    ticks = 0
    last_measure = None

    block = {}
    ip_sec = {}

    port_checking = False
    start_time_ms = None
    max_mtu_size = None
    reusable_address = None

    def __init__(self, server, socket: UDPServerSocket, max_mtu_size: int):
        self.server = server
        self.socket = socket
        self.start_time_ms = int(microtime(True) * 1000)
        self.max_mtu_size = max_mtu_size
        self.offline_message_handler = OfflineMessageHandler(self)
        self.reusable_address = copy.deepcopy(self.socket.get_bind_address())
        self.register_packets()
        self.run()

    def get_raknet_time_ms(self) -> int:
        return int((microtime(True) * 1000) - self.start_time_ms)

    def get_port(self) -> int:
        return self.socket.get_bind_address().port

    def get_max_mtu_size(self):
        return self.max_mtu_size

    def get_protocol_version(self):
        self.server.get_protocol_version()

    def run(self):
        self.tick_processor()

    def tick_processor(self):
        self.last_measure = microtime(True)
        while not self.shutdown:
            start = microtime(True)

            while self.receive_packet():
                pass
            while self.receive_stream():
                pass
            
            time_ = microtime(True) - start
            if time_ < self.RAKLIB_TIME_PER_TICK:
                time.sleep((microtime(True) + self.RAKLIB_TIME_PER_TICK - time_) - time.time())
            self.tick()

    def tick(self):
        time_ = microtime(True)
        values = list(self.sessions.values())
        for session in values:
            session.update(time_)
        for (address, count) in self.ip_sec:
            if count > self.packet_limit or count == self.packet_limit:
                self.block_address(address)
        self.ip_sec = {}

        if (self.ticks & 0b1111) == 0 or (self.ticks % self.RAKLIB_TPS) == 0:
            if self.send_bytes > 0 or self.receive_bytes > 0:
                diff = max(0.005, time_ - self.last_measure)
                self.stream_option("bandwith", json.dumps({
                    "up": self.send_bytes / diff,
                    "down": self.receive_bytes / diff
                }))
                self.send_bytes = 0
                self.receive_bytes = 0
                self.last_measure = time_

            if len(self.block) > 0:
                # TODO: Remove this?
                now = microtime(True)
                for address in self.block.keys():
                    timeout = self.block.get(address)
                    if timeout <= now:
                        del self.block[address]
                    else:
                        break
        self.ticks += 1

    def receive_packet(self) -> bool:
        data = self.socket.read_packet()
        if data is None:
            return False
        else:
            buffer, source = data
        address = self.reusable_address
        packet_length = len(buffer)
        self.receive_bytes += packet_length
        if len(buffer) < 0:
            return False
        try:
            self.ip_sec[source] += 1
        except Exception:
            self.ip_sec[source] = 1
            pass
        packet = self.get_packet_from_pool(buffer[0])
        if packet is not None:
            packet.buffer = buffer
            session = self.get_session(InternetAddress(source[0], source[1], 4))
            if session is not None:
                session.handle_packet(packet)
            return True
        elif buffer is not b"":
            self.stream_raw(InternetAddress(source[0], source[1], 4), buffer)
            return True
        else:
            return False

    def send_packet(self, packet: Packet, address: InternetAddress):
        packet.encode()
        self.send_bytes += len(packet.buffer)
        self.socket.write_packet(packet.get_buffer(), address.get_ip(), address.get_port())

    def stream_encapsulated(self, session: Session, packet: EncapsulatedPacket, flags=PyRakLib.PRIORITY_NORMAL):
        identifier = session.get_address().to_string()
        buffer = b""
        buffer += chr(PyRakLib.PACKET_ENCAPSULATED)
        buffer += chr(len(identifier))
        buffer += identifier
        buffer += chr(flags)
        buffer += packet.to_internal_binary()
        self.server.push_thread_to_main_packet(buffer)

    def stream_raw(self, address: InternetAddress, payload: bytes):
        buffer = chr(PyRakLib.PACKET_RAW)
        buffer += chr(len(address.get_ip()))
        buffer += address.get_ip()
        buffer += Binary.write_short(address.port)
        buffer += payload
        self.server.push_thread_to_main_packet(buffer)

    def stream_close(self, identifier, reason):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_CLOSE_SESSION)
        buffer += chr(len(identifier))
        buffer += identifier
        buffer += chr(len(reason))
        buffer += reason
        self.server.push_thread_to_main_packet(buffer)

    def stream_invalid(self, identifier):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_INVALID_SESSION)
        buffer += chr(len(identifier))
        buffer += identifier
        self.server.push_thread_to_main_packet(buffer)

    def stream_open(self, session):
        buffer = b""
        address = session.get_address()
        identifier = address.to_string()
        buffer += chr(PyRakLib.PACKET_OPEN_SESSION)
        buffer += chr(len(identifier))
        buffer += identifier
        buffer += chr(len(address.ip))
        buffer += Binary.write_short(address.port)
        buffer += Binary.write_long(session.get_id())
        self.server.push_thread_to_main_packet(buffer)

    def stream_ack(self, identifier, identifier_ack):
        buffer = b""
        buffer += chr(PyRakLib.PACKET_ACK_NOTIFICATION)
        buffer += chr(len(identifier))
        buffer += identifier
        buffer += Binary.write_int(identifier_ack)
        self.server.push_thread_to_main_packet(buffer)

    def stream_option(self, name, value):
        buffer = ""
        buffer += chr(PyRakLib.PACKET_SET_OPTION)
        buffer += chr(len(name))
        buffer += name
        buffer += value
        self.server.push_thread_to_main_packet(buffer.encode("UTF-8"))

    def stream_ping_measure(self, session: Session, ping_ms: int):
        identifier = session.get_address().to_string()
        buffer = b""
        buffer += chr(PyRakLib.PACKET_REPORT_PING)
        buffer += chr(len(identifier))
        buffer += identifier
        buffer += Binary.write_int(ping_ms)
        self.server.push_thread_to_main_packet(buffer)

    def receive_stream(self) -> bool:
        packet = self.server.read_main_to_thread_packet()
        if packet == b'':
            return False
        if len(packet) > 0:
            packet_id = ord(packet[0])
            offset = 1
            if packet_id == PyRakLib.PACKET_ENCAPSULATED:
                length = packet[offset]
                identifier = packet[offset:offset + length]
                offset += length
                session = self.sessions[identifier] or None
                if session is not None and session.is_connected():
                    offset += 1
                    flags = packet[offset]
                    buffer = packet[offset:]
                    session.add_encapsulated_to_queue(EncapsulatedPacket.from_internal_binary(buffer), flags)
                else:
                    self.stream_invalid(packet_id)
            elif packet_id == PyRakLib.PACKET_RAW:
                length = packet[offset]
                address = packet[offset:length]
                offset += length
                port = Binary.read_short(packet[offset:2])
                offset += 2
                payload = packet[offset:]
                self.socket.write_packet(payload, address, port)
            elif packet_id == PyRakLib.PACKET_CLOSE_SESSION:
                offset += 1
                length = packet[offset]
                packet_id = packet[offset:length]
                if packet_id in self.sessions:
                    self.sessions[packet_id].flag_for_disconnection()
                else:
                    self.stream_invalid(packet_id)
            elif packet_id == PyRakLib.PACKET_INVALID_SESSION:
                offset += 1
                length = packet[offset]
                packet_id = packet[offset:length]
                if packet_id in self.sessions:
                    self.remove_session(self.sessions[packet_id])
            elif packet_id == PyRakLib.PACKET_SET_OPTION:
                length = ord(packet[offset])
                offset += 1
                name = packet[offset:offset + length]
                offset += length
                value = packet[offset:]
                if name == "servername":
                    # print(name+b" "+value)
                    self.name = value
                elif name == "portChecking":
                    self.port_checking = bool(value)
                elif name == "packetLimit":
                    self.packet_limit = int(value)
                else:
                    pass
                    # self.server.logger.error("Invalid option: "+name+" "+value)
            elif packet_id == PyRakLib.PACKET_BLOCK_ADDRESS:
                offset += 1
                length = packet[offset]
                address = packet[offset:length]
                offset += length
                timeout = Binary.read_int(packet[offset:4])
                self.block_address(address, timeout)
            elif packet_id == PyRakLib.PACKET_UNBLOCK_ADDRESS:
                offset += 1
                length = packet[offset]
                address = packet[offset:length]
                self.unblock_address(address)
            elif packet_id == PyRakLib.PACKET_SHUTDOWN:
                for session in self.sessions:
                    self.remove_session(session)
                self.socket.close()
                self.shutdown = True
            elif packet_id == PyRakLib.PACKET_EMERGENCY_SHUTDOWN:
                self.shutdown = True
            else:
                print("Unknown raklib internal packet " + str(packet_id))
            return True
        return False

    def block_address(self, address: bytes, timeout=300):
        final = microtime(True) + timeout
        for (i, block) in enumerate(self.block):
            if i == address:  # Isset
                if block < final:
                    self.block[i] = final
                    return
        self.block[address] = final

    def unblock_address(self, address: bytes):
        try:
            del self.block[address]
        except(NameError, IndexError):
            print("Unknown address to unblock")
            pass

    def get_session(self, address: InternetAddress) -> Session:
        try:
            return self.sessions[address.to_string()]
        except (KeyError, IndexError, NameError):
            self.sessions[address.to_string()] = Session(self, address, self.get_id(), self.get_max_mtu_size())
            return self.sessions[address.to_string()]

    def session_exists(self, address: InternetAddress):
        return address.to_string() in self.sessions

    def create_session(self, address: InternetAddress, client_id: int, mtu_size: int) -> Session:
        self.check_sessions()

        self.sessions[address.to_string()] = session = Session(self, copy.deepcopy(address), client_id, mtu_size)
        return session

    def remove_session(self, session: Session, reason="unknown"):
        identity = session.get_address().to_string()
        try:
            self.sessions[identity].close()
            self.remove_session_internal(session)
            self.stream_close(identity, reason)
        except NameError or KeyError:
            pass

    def remove_session_internal(self, session: Session):
        try:
            del self.sessions[session.get_address().to_string()]
        except IndexError:
            pass

    def open_session(self, session):
        self.stream_open(session)

    def check_sessions(self):
        if len(self.sessions) > 4096:
            for (i, session) in enumerate(self.sessions):
                if session.is_temporal():
                    self.sessions.pop(i)
                    if len(self.sessions) <= 4096:
                        break

    def notify_ack(self, session: Session, identifier_ack):
        self.stream_ack(session.get_address().to_string(), identifier_ack)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.server.get_server_id()

    def register_packet(self, packet_id, packet_class):
        self.packet_pool[packet_id] = packet_class()

    def get_packet_from_pool(self, packet_id, buffer=b"") -> Packet:
        try:
            pk = copy.deepcopy(self.packet_pool[packet_id])
            if pk is not None:
                pk.buffer = buffer
            return pk
        except(IndexError, NameError):
            return None

    def register_packets(self):
        self.register_packet(UnconnectedPing.ID, UnconnectedPing)
        self.register_packet(UnconnectedPingOpenConnections.ID, UnconnectedPingOpenConnections)
        self.register_packet(OpenConnectionRequest1.ID, OpenConnectionRequest1)
        self.register_packet(OpenConnectionRequest2.ID, OpenConnectionRequest2)
        self.register_packet(OpenConnectionReply1.ID, OpenConnectionReply1)
        self.register_packet(OpenConnectionReply2.ID, OpenConnectionReply2)
        self.register_packet(UnconnectedPong.ID, UnconnectedPong)
        self.register_packet(AdvertiseSystem.ID, AdvertiseSystem)
