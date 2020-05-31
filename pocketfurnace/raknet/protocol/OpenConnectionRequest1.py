
from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.OfflineMessage import OfflineMessage


class OpenConnectionRequest1(OfflineMessage):
    ID = MessageIdentifiers.ID_OPEN_CONNECTION_REQUEST_1

    protocol = PyRakLib.DEFAULT_PROTOCOL_VERSION
    mtu_size = None

    def _encodePayload(self):
        self._write_magic()
        self.put_byte(self.protocol)
        self.buffer.ljust(self.mtu_size, b"\x00")

    def _decodePayload(self):
        self._read_magic()
        self.protocol = self.get_byte()
        self.mtu_size = len(self.buffer)
