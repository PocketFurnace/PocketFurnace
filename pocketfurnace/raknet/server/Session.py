import collections
import copy
import math
import time as time_
from collections import deque

from pocketfurnace.raknet import PyRakLib
from pocketfurnace.raknet.protocol import DisconnectionNotification
from pocketfurnace.raknet.protocol.ACK import ACK
from pocketfurnace.raknet.protocol.ConnectedPing import ConnectedPing
from pocketfurnace.raknet.protocol.ConnectedPong import ConnectedPong
from pocketfurnace.raknet.protocol.ConnectionRequest import ConnectionRequest
from pocketfurnace.raknet.protocol.ConnectionRequestAccepted import ConnectionRequestAccepted
from pocketfurnace.raknet.protocol.Datagram import Datagram
from pocketfurnace.raknet.protocol.DisconnectionNotification import DisconnectNotification
from pocketfurnace.raknet.protocol.EncapsulatedPacket import EncapsulatedPacket
from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.NACK import NACK
from pocketfurnace.raknet.protocol.NewIncomingConnection import NewIncomingConnection
from pocketfurnace.raknet.protocol.Packet import Packet
from pocketfurnace.raknet.protocol.PacketReliability import PacketReliability
from pocketfurnace.raknet.server import SessionManager
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress


def microtime(get_as_float=False):
    if get_as_float:
        return time_.time()
    return '%f %d' % math.modf(time_.time())


def str_split(s, n) -> list:
    ret = []
    for i in range(0, len(s), n):
        ret.append(s[i:i+n])
    return ret


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


def is_in_list(item, indexed_list: deque) -> bool:
    try:
        return item in indexed_list
        # indexed_list[item]
        # return True
    except NameError:
        return False
    except IndexError:
        return False
    except KeyError:
        return False


class Session:
    STATE_CONNECTING = 0
    STATE_CONNECTED = 1
    STATE_DISCONNECTING = 2
    STATE_DISCONNECTED = 3

    MIN_MTU_SIZE = 400

    MAX_SPLIT_SIZE = 128
    MAX_SPLIT_COUNT = 4

    CHANNEL_COUNT = 32

    WINDOW_SIZE = 2048

    message_index = 0
    send_ordered_index = []
    send_sequenced_index = []
    receive_ordered_index = []
    receive_sequenced_highest_index = []
    receive_ordered_packets = []

    session_manager = None
    address = None
    state = STATE_CONNECTING
    mtu_size = 548  # Min size
    __id = 0
    split_id = 0

    send_seq_number = 0
    last_update = None
    disconnection_time = None
    __is_temporal = True
    packet_to_send = []
    is_active = False

    """@:type collections.deque"""
    ack_queue = collections.deque()

    """@:type collections.deque"""
    nack_queue = collections.deque()

    recovery_queue = {}

    split_packets = []

    need_ack = []

    __send_queue = None

    window_start = None
    window_end = None

    highest_seq_number_this_tick = -1

    """@:type collections.deque"""
    received_window = collections.deque()

    reliable_window_start = None
    reliable_window_end = None
    reliable_window = {}
    last_ping_time = -1
    last_ping_measure = 1
    last_reliable_index = -1

    def __init__(self, session_manager: SessionManager, address: InternetAddress, client_id: int, mtu_size: int):
        if mtu_size < self.MIN_MTU_SIZE:
            raise ValueError("MTU size must be at least " + str(self.MIN_MTU_SIZE) + " got " + str(mtu_size))

        self.session_manager = session_manager
        self.address = address
        self.__id = client_id
        self.__send_queue = Datagram()
        self.last_update = microtime(True)
        self.is_active = False
        self.window_start = 0
        self.window_end = self.WINDOW_SIZE
        self.reliable_window_start = 0
        self.reliable_window_end = self.WINDOW_SIZE
        self.send_ordered_index = [index for index in range(0, self.CHANNEL_COUNT)]
        self.send_sequenced_index = [index for index in range(0, self.CHANNEL_COUNT)]
        self.receive_ordered_index = [index for index in range(0, self.CHANNEL_COUNT)]
        self.receive_sequenced_highest_index = [index for index in range(0, self.CHANNEL_COUNT)]
        self.receive_ordered_packets = [[] for index in range(0, self.CHANNEL_COUNT)]
        self.mtu_size = mtu_size

    def get_address(self) -> InternetAddress:
        return self.address

    def get_id(self) -> int:
        return self.__id

    def get_state(self) -> int:
        return self.state

    def is_temporal(self) -> bool:
        return self.__is_temporal

    def is_connected(self) -> bool:
        return self.state != self.STATE_DISCONNECTING and self.state != self.STATE_DISCONNECTED

    def update(self, time):
        if not self.is_active and self.last_update + 10 < time:
            self.disconnect("timeout")
            return

        if self.state == self.STATE_DISCONNECTING and (len(self.__send_queue.packets) == 0) and (len(self.ack_queue) == 0) and (len(self.nack_queue) == 0) and (len(self.packet_to_send) == 0) and (len(self.recovery_queue) == 0) or self.disconnection_time + 10 < time:
            self.close()
            return

        self.is_active = False
        diff = self.highest_seq_number_this_tick - self.window_start + 1
        assert diff >= 0
        if diff > 0:
            self.window_start += diff
            self.window_end += diff

        if len(self.ack_queue) > 0:
            pk = ACK()
            pk.packets = self.ack_queue
            self.send_packet(pk)
            self.ack_queue.clear()

        if len(self.nack_queue) > 0:
            pk = NACK()
            pk.packets = self.nack_queue
            self.send_packet(pk)
            self.nack_queue.clear()

        if len(self.packet_to_send) > 0:
            limit = 16
            for (k, pk) in enumerate(self.packet_to_send):
                self._send_datagram(pk)
                self.packet_to_send.remove(k)

                if --limit <= 0:
                    break

            if len(self.packet_to_send) > self.WINDOW_SIZE:
                self.packet_to_send.clear()

        if len(self.need_ack) > 0:
            for (identifier_ack, indexes) in enumerate(self.need_ack):
                if len(indexes) == 0:
                    self.need_ack.remove(identifier_ack)
                    self.session_manager.notify_ack(self, identifier_ack)

        for seq in copy.deepcopy(self.recovery_queue).keys():
            pk = self.recovery_queue.get(seq)
            if pk.send_time is None:
                self.packet_to_send.append(pk)
                del self.recovery_queue[seq]
                continue
            if pk.sendTime < (int(time_.time()) - 8):
                self.packet_to_send.append(pk)
                del self.recovery_queue[seq]
            else:
                break

        if self.last_ping_time + 5 < time:
            self._send_ping()
            self.last_ping_time = time
        self.send_queue()

    def disconnect(self, reason="unknown"):
        self.session_manager.remove_session(self, reason)

    def _send_datagram(self, datagram: Datagram):
        if datagram.seq_number is not None:
            del self.recovery_queue[datagram.seq_number]
        datagram.seq_number = self.send_seq_number + 1
        datagram.send_time = microtime(True)
        self.recovery_queue.update({datagram.seq_number: datagram})
        self.send_packet(datagram)

    def _queue_connected_packet(self, packet: Packet, reliability: int, order_channel: int, flags: int):
        packet.encode()
        encapsulated = EncapsulatedPacket()
        encapsulated.reliability = reliability
        encapsulated.order_channel = order_channel
        encapsulated.buffer = packet.get_buffer()
        self.add_encapsulated_to_queue(encapsulated, flags)

    def send_packet(self, packet: Packet):
        self.session_manager.send_packet(packet, self.address)

    def send_queue(self):
        if len(self.__send_queue.packets) > 0:
            self._send_datagram(self.__send_queue)
            self.__send_queue = Datagram()

    def _send_ping(self, reliability=PacketReliability.UNRELIABLE):
        pk = ConnectedPing()
        pk.send_ping_time = self.session_manager.get_raknet_time_ms()
        self._queue_connected_packet(pk, reliability, 0, PyRakLib.PRIORITY_IMMEDIATE)

    def add_to_queue(self, pk: EncapsulatedPacket, flags=PyRakLib.PRIORITY_NORMAL):
        priority = flags & 0b00000111
        if pk.need_ack and pk.message_index is not None:
            self.need_ack[pk.identifier_ack][pk.message_index] = pk.message_index
        length = self.__send_queue.length()
        if length + pk.get_total_length() > self.mtu_size - 36:
            # IP header (20 bytes) + UDP header (8 bytes) + RakNet weird (8 bytes) = 36 bytes
            self.send_queue()
        if pk.need_ack:
            self.__send_queue.packets.append(copy.deepcopy(pk))
            pk.need_ack = False
        else:
            self.__send_queue.packets.append(pk.to_binary())
        if priority == PyRakLib.PRIORITY_IMMEDIATE:  # Skip queues
            self.send_queue()

    def add_encapsulated_to_queue(self, packet: EncapsulatedPacket, flags=PyRakLib.PRIORITY_NORMAL):
        packet.need_ack = (flags & PyRakLib.FLAG_NEED_ACK)
        if packet.need_ack > 0:
            self.need_ack[packet.identifier_ack] = []
        if PacketReliability.is_ordered(packet.reliability):
            packet.order_index = self.send_ordered_index[packet.order_channel] + 1
        elif PacketReliability.is_sequenced(packet.reliability):
            packet.order_index = self.send_ordered_index[packet.order_channel]
            packet.sequence_index = self.send_sequenced_index[packet.order_channel] + 1
        # IP header size (20 bytes) + UDP header size (8 bytes) + RakNet weird (8 bytes) + datagram header size (4 bytes) + max encapsulated packet header size (20 bytes)
        max_size = self.mtu_size - 60
        if len(packet.buffer) > max_size:
            buffers = str_split(packet.buffer, max_size)
            assert(buffers is not False)
            buffer_count = len(buffers)
            self.split_id += 1
            split_id = self.split_id % 65536
            for (count, buffer) in enumerate(buffers):
                pk = EncapsulatedPacket()
                pk.split_id = split_id
                pk.has_split = True
                pk.split_count = buffer_count
                pk.reliability = packet.reliability
                pk.split_index = count
                pk.buffer = buffer
                if PacketReliability.is_reliable(pk.reliability):
                    self.message_index += 1
                    pk.message_index = self.message_index
                else:
                    pk.message_index = packet.message_index
                pk.sequence_index = packet.sequence_index
                pk.order_channel = packet.order_channel
                pk.order_index = packet.order_index
                self.add_to_queue(pk, flags | PyRakLib.PRIORITY_IMMEDIATE)
        else:
            if PacketReliability.is_reliable(packet.reliability):
                packet.message_index = self.message_index + 1
            self.add_to_queue(packet, flags)

    def _handle_split(self, packet: EncapsulatedPacket):
        if packet.split_count >= self.MAX_SPLIT_SIZE or packet.split_count < 0 or packet.split_index >= packet.split_count or packet.split_index < 0:
            # self.session_manager.get_logger.debug()
            return
        if packet.split_id in  self.split_packets:
            if len(self.split_packets) >= self.MAX_SPLIT_COUNT:
                # DEBUG IGNORED SPLIT PART
                return
            self.split_packets.insert(packet.split_id, [None for i in range(0, packet.split_count)])
        elif len(self.split_packets[packet.split_id]) != packet.split_count:
            print("[Session] Wrong split count")
            return
        self.split_packets[packet.split_id][packet.split_index] = packet

        for (split_index, part) in enumerate(self.split_packets[packet.split_id]):
            if part is None:
                return None
        # got all parts, reassemble the packet
        pk = EncapsulatedPacket()
        pk.buffer = b""
        pk.reliability = packet.reliability
        pk.message_index = packet.message_index
        pk.sequence_index = packet.sequence_index
        pk.order_index = packet.order_index
        pk.order_channel = packet.order_channel

        for i in range(0, packet.split_count):
            pk.buffer += self.split_packets[packet.split_id][i].buffer

        pk.length = len(pk.buffer)
        self.split_packets.remove(packet.split_id)
        return pk

    def handle_encapsulated_packet(self, packet: EncapsulatedPacket):
        if packet.message_index is not None:
            # check for duplicates or out of range
            if packet.message_index < self.reliable_window_start or packet.message_index > self.reliable_window_end or packet.message_index in self.reliable_window:
                return
            self.reliable_window[packet.message_index] = True

            if packet.message_index == self.reliable_window_start:
                try:
                    for reliable_window in self.reliable_window[self.reliable_window_start]:
                        self.reliable_window_start += 1
                        del self.reliable_window[reliable_window]
                        self.reliable_window_end += 1
                except (NameError, IndexError):
                    pass
        packet_split = self._handle_split(packet)
        if packet.has_split and packet_split is None:
            return

        if PacketReliability.is_sequenced_or_ordered(packet.reliability) and packet.order_channel >= self.CHANNEL_COUNT:
            # TODO: this should result in peer banning
            # DEBUG INVALID PACKET
            return
        if PacketReliability.is_sequenced(packet.reliability):
            if packet.sequence_index < self.receive_sequenced_highest_index[packet.order_channel] or packet.order_index < self.receive_ordered_index[packet.order_channel]:
                # too old sequenced packet, discard it
                return
            self.receive_sequenced_highest_index.insert(packet.order_channel, packet.sequence_index + 1)
            self.handle_encapsulated_packet_route(packet)
        elif PacketReliability.is_ordered(packet.reliability):
            if packet.order_index == self.receive_ordered_index[packet.order_channel]:
                self.receive_sequenced_highest_index.insert(packet.order_index, 0)
                self.receive_ordered_index.insert(packet.order_channel, packet.order_index + 1)
                self.handle_encapsulated_packet_route(packet)
                i = self.receive_ordered_index[packet.order_channel]
                for key in self.receive_ordered_packets[packet.order_channel][i]:
                    self.handle_encapsulated_packet_route(key)
                    del key
                self.receive_ordered_index.insert(packet.order_channel, i)
            elif packet.order_index > self.receive_ordered_index[packet.order_channel]:
                self.receive_ordered_packets[packet.order_channel].insert(packet.order_index, packet)
            else:
                # dupplicate/already received packet
                pass
        else:
            self.handle_encapsulated_packet_route(packet)

    def handle_encapsulated_packet_route(self, packet: EncapsulatedPacket):
        if self.session_manager is None:
            return
        if packet.has_split:
            if self.state == self.STATE_CONNECTED:
                self._handle_split(packet)
            return

        packet_id = ord(packet.buffer[0])
        if packet_id < MessageIdentifiers.ID_USER_PACKET_ENUM:  # internal data packet
            if self.state == self.STATE_CONNECTING:
                if packet_id == ConnectionRequest.ID:
                    data_packet = ConnectionRequest(packet.buffer)
                    data_packet.decode()

                    pk = ConnectionRequestAccepted()
                    pk.address = self.address
                    pk.send_ping_time = data_packet.send_ping_time
                    pk.send_pong_time = self.session_manager.get_raknet_time_ms()
                    self._queue_connected_packet(pk, PacketReliability.UNRELIABLE, 0, PyRakLib.PRIORITY_IMMEDIATE)
                elif packet_id == NewIncomingConnection.ID:
                    data_packet = NewIncomingConnection(packet.buffer)
                    data_packet.decode()

                    if data_packet.address.port == self.session_manager.get_port() or not self.session_manager.port_checking:
                        self.state = self.STATE_CONNECTED  # FINALLY!
                        self.__is_temporal = False
                        self.session_manager.open_session(self)
                        self._send_ping()

            elif packet_id == DisconnectionNotification.ID:
                self.disconnect("client disconnect")
            elif packet_id == ConnectedPing.ID:
                data_packet = ConnectedPing(packet.buffer)
                data_packet.decode()

                pk = ConnectedPong()
                pk.send_ping_time = data_packet.send_ping_time
                pk.send_pong_time = self.session_manager.get_raknet_time_ms()
                self._queue_connected_packet(pk, PacketReliability.UNRELIABLE, 0)
            elif packet_id == ConnectedPong.ID:
                data_packet = ConnectedPong(packet.buffer)
                data_packet.decode()
                self.handle_pong(data_packet.send_ping_time, data_packet.send_pong_time)
        elif self.state == self.STATE_CONNECTED:
            self.session_manager.stream_encapsulated(self, packet)
        else:
            pass

    def handle_pong(self, send_ping_time: int, send_pong_time: int):
        self.last_ping_measure = self.session_manager.get_raknet_time_ms() - send_ping_time
        self.session_manager.stream_ping_measure(self, self.last_ping_measure)

    def handle_packet(self, packet: Packet):
        self.is_active = True
        self.last_update = microtime(True)
        if isinstance(packet, Datagram):
            packet.decode()
            if packet.seq_number < self.window_start or packet.seq_number > self.window_end or packet.seq_number in self.ack_queue:
                # TODO: DEBUG RECEIVE DUPLICATE OR OUT OF WINDOW
                return
            if is_in_list(packet.seq_number, self.nack_queue):
                self.nack_queue.remove(packet.seq_number)
            self.ack_queue.insert(packet.seq_number, packet.seq_number)
            if self.highest_seq_number_this_tick < packet.seq_number:
                self.highest_seq_number_this_tick = packet.seq_number
            if packet.seq_number == self.window_start:
                for window in self.ack_queue:
                    if self.window_start in self.ack_queue:
                        self.window_end += 1
            elif packet.seq_number > self.window_start:
                i = self.window_start
                while i < packet.seq_number:
                    if i not in self.ack_queue:
                        self.nack_queue.insert(i, i)
                    i += 1
            else:
                assert False, "received packet before window start"
            for pk in packet.packets:
                assert isinstance(pk, EncapsulatedPacket)
                self.handle_encapsulated_packet(pk)
        else:
            if isinstance(packet, ACK):
                packet.decode()
                for seq in packet.packets:
                    if seq in self.recovery_queue:
                        for (packets, pk) in enumerate(self.recovery_queue[seq]):
                            if isinstance(pk, EncapsulatedPacket) and pk.need_ack and pk.message_index is not None:
                                del self.need_ack[pk.identifier_ack][pk.message_index]
                        del self.recovery_queue[seq]
            elif isinstance(packet, NACK):
                packet.decode()
                for seq in packet.packets:
                    if seq in self.recovery_queue:
                        self.packet_to_send.append(self.recovery_queue[seq])

    def flag_for_disconnection(self):
        self.state = self.STATE_DISCONNECTING
        self.disconnection_time = microtime(True)

    def close(self):
        if self.state != self.STATE_DISCONNECTED:
            self.state = self.STATE_DISCONNECTED
            self._queue_connected_packet(DisconnectNotification(), PacketReliability.RELIABLE_ORDERED, 0, PyRakLib.PRIORITY_IMMEDIATE)
        self.session_manager.remove_session_internal(self)
