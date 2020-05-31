from abc import ABCMeta, abstractmethod

from pocketfurnace.raknet.protocol.EncapsulatedPacket import EncapsulatedPacket


class ServerInstance:
    __metaclass__ = ABCMeta

    @abstractmethod
    def open_session(self, identifier: str, address: str, port: int, client_id: int): pass

    @abstractmethod
    def close_session(self, identifier: str, reason: str): pass

    @abstractmethod
    def handle_encapsulated(self, identifier: str, packet: EncapsulatedPacket, flags: int): pass

    @abstractmethod
    def handle_raw(self, address: str, port: int, payload): pass

    @abstractmethod
    def notify_ack(self, identifier: str, identifier_ack: int): pass

    @abstractmethod
    def handle_option(self, option: str, value: str): pass

    @abstractmethod
    def update_ping(self, identifier: str, ping_ms: int): pass
