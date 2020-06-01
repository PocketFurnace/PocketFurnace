from abc import ABCMeta, abstractmethod

from pocketfurnace.raknet.utils.InternetAddress import InternetAddress
from pocketfurnace.utils.BinaryStream import BinaryStream


class Packet(BinaryStream):
    __metaclass__ = ABCMeta
    ID = -1
    send_time = None

    def get_string(self) -> bytes:
        return self.get(self.get_short())

    def get_address(self) -> InternetAddress:
        version = self.get_byte()
        if version == 4:
            address = str(((~self.get_byte()) & 0xff)) + "." + str(((~self.get_byte()) & 0xff)) + "." + str(((~self.get_byte()) & 0xff)) + "." + str(((~self.get_byte()) & 0xff))
            port = self.get_short()
            return InternetAddress(address, port, version)
        elif version == 6:
            pass  # TODO: add IPv6 support
        else:
            raise ValueError("Unknown IP address version " + str(version))

    def put_string(self, string: bytes):
        self.put_short(len(string))
        self.put(string)

    def put_address(self, address: InternetAddress):
        self.put_byte(address.version)
        if address.version == 4:
            for s in str(address.ip).split("."):
                self.put_byte((~(int(s))) & 0xff)
            self.put_short(address.port)
        elif address.version == 6:
            pass  # TODO: add IPv6 support
        else:
            raise ValueError("Unknown IP address version " + str(address.version))

    def encode(self):
        self.reset()
        self._encodeHeader()
        self._encodePayload()

    def _encodeHeader(self):
        self.put_byte(self.ID)

    @abstractmethod
    def _encodePayload(self):
        pass

    def decode(self):
        self.offset = 0
        self._decodeHeader()
        self._decodePayload()

    def _decodeHeader(self):
        return self.get_byte()  # PID

    @abstractmethod
    def _decodePayload(self):
        pass

    def clean(self):
        self.buffer = b""
        self.offset = 0
        self.send_time = None
        return self
