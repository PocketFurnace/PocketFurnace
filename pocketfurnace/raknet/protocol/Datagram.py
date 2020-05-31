from pocketfurnace.raknet.protocol.EncapsulatedPacket import EncapsulatedPacket
from pocketfurnace.raknet.protocol.Packet import Packet


class Datagram(Packet):

    BITFLAG_VALID = 0x80
    BITFLAG_ACK = 0x40
    BITFLAG_NACK = 0x20
    BITFLAG_PACKET_PAIR = 0x10
    BITFLAG_CONTINUOS_SEND = 0x08
    BITFLAG_NEEDS_B_AND_AS = 0x04

    header_flags = 0
    packets = []
    seq_number = None

    def _encodeHeader(self):
        self.put_byte(self.BITFLAG_VALID | self.header_flags)

    def _encodePayload(self):
        self.put_l_triad(self.seq_number)
        for packet in self.packets:
            self.put(packet.to_binary() if isinstance(packet, EncapsulatedPacket) else packet)

    def length(self) -> int:
        length = 4
        for packet in self.packets:
            if isinstance(packet, EncapsulatedPacket):
                length += packet.get_total_length()
            else:
                length += len(packet)
        return length

    def _decodeHeader(self):
        self.header_flags = self.get_byte()

    def _decodePayload(self):
        self.seq_number = self.get_l_triad()
        while not self.feof():
            offset = 0
            data = self.buffer[offset:]
            packet = EncapsulatedPacket.from_binary(data, offset)
            self.offset += offset
            if packet.buffer == b"":
                break
            self.packets.append(packet)

    def clean(self):
        self.packets = []
        self.seq_number = None
        return super().clean()
