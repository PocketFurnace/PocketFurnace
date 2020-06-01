from abc import ABC

from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.protocol.Packet import Packet


class OfflineMessage(Packet, ABC):
    magic = None

    def _read_magic(self):
        self.magic = self.get(16)

    def _write_magic(self):
        self.put(PyRakLib.MAGIC)

    def is_valid(self):
        return self.magic == PyRakLib.MAGIC
