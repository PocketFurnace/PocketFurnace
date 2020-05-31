from abc import ABC

from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.protocol.Packet import Packet
from pprint import pprint


class OfflineMessage(Packet, ABC):
    _magic = None

    def _read_magic(self):
        self._magic = self.get(16)

    def _write_magic(self):
        self.put(PyRakLib.MAGIC)

    def is_valid(self):
        return self._magic == PyRakLib.MAGIC
