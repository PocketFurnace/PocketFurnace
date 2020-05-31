from pocketfurnace.raknet.protocol.Network import Network
from pocketfurnace.raknet.server import ServerHandler
from pocketfurnace.raknet.server.ServerInstance import ServerInstance
from ..AdvancedSourceInterface import AdvancedSourceInterface
from ...Server import Server
from pocketfurnace.raknet.server.PyRakLibServer import PyRakLibServer


class RakLibInterface(AdvancedSourceInterface, ServerInstance):
    MCPE_RAKNET_PROTOCOL_VERSION = 9

    __server = None
    __network = None
    __raklib = None
    __players = []
    __identifiers = []
    __identifiers_ack = []
    __interface = None

    def __init__(self, server: Server):
        self.__server = server
        self.__raklib = PyRakLibServer(port=19132)
        self.__interface = ServerHandler(self.__raklib, None)
        self.start()

    def start(self):
        self.__raklib.start()

    def set_network(self, network: Network):
        self.__network = network
