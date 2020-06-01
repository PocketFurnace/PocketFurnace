from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.Packet import Packet
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress


class ConnectionRequestAccepted(Packet):
    ID = MessageIdentifiers.ID_CONNECTION_REQUEST_ACCEPTED
    address = None
    system_addresses = []
    send_ping_time = None
    send_pong_time = None

    def __init__(self, buffer: bytes = b"", offset: int = 0):
        super().__init__(buffer, offset)
        self.system_addresses.append(InternetAddress("127.0.0.1", 0, 4))

    def _encodePayload(self):
        i = 0
        self.put_address(self.address)
        self.put_short(0)
        dummy = InternetAddress("0.0.0.0", 0, 4)
        while i < PyRakLib.SYSTEM_ADDRESS_COUNT:
            self.put_address(self.system_addresses[i] or dummy)
            i += 1
        self.put_long(self.send_ping_time)
        self.put_long(self.send_pong_time)

    def _decodePayload(self):
        i = 0
        self.address = self.get_address()
        self.get_short()  # TODO: check this
        length = len(self.buffer)
        dummy = InternetAddress("0.0.0.0", 0, 4)
        while i < PyRakLib.SYSTEM_ADDRESS_COUNT:
            try:
                self.system_addresses.insert(i, self.get_address() if self.offset + 16 < length else dummy)
            except IndexError:
                pass
            i += 1
        self.send_ping_time = self.get_long()
        self.send_pong_time = self.get_long()
