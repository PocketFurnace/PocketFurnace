from pocketfurnace.raknet.protocol.PacketReliability import PacketReliability
from pocketfurnace.utils.Binary import Binary
from math import ceil


class EncapsulatedPacket:

    RELIABILITY_SHIFT = 5
    RELIABILITY_FLAGS = 0b111 << RELIABILITY_SHIFT
    SPLIT_FLAG = 0b00010000
    reliability = None
    has_split = False
    length = 0
    message_index = None
    sequence_index = None
    order_index = None
    order_channel = None
    split_count = None
    split_id = None
    split_index = None
    buffer = b""
    need_ack = False
    identifier_ack = None

    @staticmethod
    def from_internal_binary(binary_bytes: bytes, offset=0):
        packet = EncapsulatedPacket()
        offset += 1
        packet.reliability = binary_bytes[offset]
        length = Binary.read_int(binary_bytes[offset:4])
        offset += 4
        packet.identifier_ack = Binary.read_int(binary_bytes[offset:4])  # TODO: don't read this for non-ack-receipt reliabilities
        offset += 4
        if PacketReliability.is_sequenced_or_ordered(packet.reliability):
            offset += 1
            packet.order_channel = binary_bytes[offset]
        packet.buffer = binary_bytes[offset:length]
        offset += length
        return packet

    def to_internal_binary(self) -> bytes:
        buffer = b""
        buffer += chr(self.reliability)
        buffer += Binary.write_int(len(self.buffer))
        buffer += Binary.write_int(self.identifier_ack or -1)
        buffer += (PacketReliability.is_sequenced_or_ordered(self.reliability if chr(self.order_channel) else b""))
        buffer += self.buffer
        return buffer

    @staticmethod
    def from_binary(binary: bytes, offset: int = 0):
        packet = EncapsulatedPacket()
        flags = binary[0]
        reliability = (flags & 0b111 << 5) >> 5
        has_split = (flags & 0b00010000) > 0
        packet.reliability = reliability
        packet.has_split = has_split
        length = int(ceil(Binary.read_short(binary[1:2])) / 8)
        offset = 3
        if PacketReliability.is_reliable(reliability):
            packet.message_index = Binary.read_l_triad(binary[offset:3])
            offset += 3
        if PacketReliability.is_sequenced(reliability):
            packet.sequence_index = Binary.read_l_triad(binary[offset:3])
            offset += 3
        if PacketReliability.is_sequenced_or_ordered(reliability):
            packet.order_index = Binary.read_l_triad(binary[offset:3])
            offset += 3
            packet.order_channel = binary[offset + 1]
        if has_split:
            packet.split_count = Binary.read_int(binary[offset:4])
            offset += 4
            packet.split_id = Binary.read_short(binary[offset:2])
            offset += 2
            packet.split_index = Binary.read_int(binary[offset:4])
            offset += 4
        packet.buffer = binary[offset:length]
        offset += length
        return packet

    def to_binary(self):
        buffer = b""
        buffer += (self.reliability << self.RELIABILITY_SHIFT) | (self.SPLIT_FLAG if self.has_split else 0)
        buffer += Binary.write_short(len(self.buffer) << 3)
        buffer += Binary.write_l_triad(self.message_index) if PacketReliability.is_reliable(self.reliability) else b""
        buffer += Binary.write_l_triad(self.sequence_index) if PacketReliability.is_sequenced(self.reliability) else b""
        buffer += Binary.write_l_triad(self.order_index + chr(self.order_channel)) if PacketReliability.is_sequenced_or_ordered(self.reliability) else b""
        buffer += Binary.write_int(self.split_count) + Binary.write_short(self.split_id) + Binary.write_int(self.split_index) if self.has_split else b""
        return buffer + self.buffer

    def get_total_length(self):
        return 1 + 1 + (3 if PacketReliability.is_reliable(self.reliability) else 0) + \
               (3 if PacketReliability.is_sequenced(self.reliability) else 0) + \
               (3 + 1 if PacketReliability.is_sequenced_or_ordered(self.reliability) else 0) + \
               (4 + 2 + 4 if self.has_split else 0) + len(self.buffer)

    def to_string(self) -> bytes:
        return self.to_binary()
