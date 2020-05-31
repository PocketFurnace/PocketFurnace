from abc import ABCMeta, abstractmethod

from pocketfurnace.network.SourceInterface import SourceInterface


class AdvancedSourceInterface(SourceInterface):

    __metaclass__ = ABCMeta

    @abstractmethod
    def block_address(self, address: str, timeout: int) -> None: pass

    @abstractmethod
    def unblock_address(self, address) -> None: pass

    @abstractmethod
    def set_network(self, network) -> None: pass

    @abstractmethod
    def send_raw_packet(self, address: str, port: int, payload: bytearray): pass
