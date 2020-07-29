import zlib

from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo
from pocketfurnace.utils.Binary import Binary


class BatchPacket(DataPacket):
    NID = ProtocolInfo.BATCH_PACKET

    payload = ""
    compressionLevel = 7

    def can_be_batched(self):
        return False

    def can_be_sent_before_login(self):
        return True

    def decode_header(self):
        pid = self.get_byte()
        assert pid == self.NID

    def decode_payload(self):
        data = self.get_remaining()
        try:
            self.payload = zlib.decompress(data, 1024 * 1024 * 2)
        except:
            self.payload = ""

    def encode_header(self):
        self.put_byte(self.NID)

    def encode_payload(self):
        compress = zlib.compressobj(self.compressionLevel, zlib.DEFLATED, -zlib.MAX_WBITS)
        compressedData = compress.compress(self.payload)
        compressedData += compress.flush()
        self.put(compressedData)

    def add_packet(self, packet: DataPacket):
        if not packet.can_be_batched():
            raise Exception(str(type(packet).__name__) + " cannot be put inside a BatchPacket")
        if not packet.isEncoded:
            packet.encode()
        self.payload += Binary.write_unsigned_var_int(len(packet.buffer)) + packet.buffer

    def get_packets(self):
        stream = DataPacket.BinaryStream(self.payload)
        count = 0
        while not stream.feof():
            count += 1
            if count >= 500:
                raise Exception("Too many packets in a single batch")
            yield stream.getString()

    def get_compression_level(self):
        return self.compressionLevel

    def set_compression_level(self, level: int):
        self.compressionLevel = level
