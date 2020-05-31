from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.protocol.MessageIdentifiers import MessageIdentifiers
from pocketfurnace.raknet.protocol.Packet import Packet
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress
from copy import deepcopy


class NewIncomingConnection(Packet):
    ID = MessageIdentifiers.ID_NEW_INCOMING_CONNECTION
    address = None
    system_addresses = []
    send_ping_time = None
    send_pong_time = None

    def _encodePayload(self):
        self.put_address(self.address)
        for address in self.system_addresses:
            self.put_address(address)
        self.put_long(self.send_ping_time)
        self.put_long(self.send_pong_time)

    def _decodePayload(self):
        self.address = self.get_address()
        # TODO: HACK!
        stop_offset = len(self.buffer) - 16
        dummy = InternetAddress("0.0.0.0", 0, 4)
        i = 0
        while i < PyRakLib.SYSTEM_ADDRESS_COUNT:
            if self.offset >= stop_offset:
                self.system_addresses.insert(i, deepcopy(dummy))
            else:
                self.system_addresses.insert(i, self.get_address())
            i += 1
        self.send_ping_time = self.get_long()
        self.send_pong_time = self.get_long()
