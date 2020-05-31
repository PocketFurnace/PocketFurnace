import atexit
import gc
import logging
import os
import queue
import random
import sys
from threading import Thread

from pocketfurnace.raknet.PyRakLib import PyRakLib
from pocketfurnace.raknet.server.SessionManager import SessionManager
from pocketfurnace.raknet.server.UDPServerSocket import UDPServerSocket
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress


class PyRakLibServer(Thread):
    address = None
    logger = None
    _shutdown = False
    external_queue = []
    internal_queue = []
    main_path = None
    server_id = 0
    max_mtu_size = None
    protocol_version = None

    def __init__(self, address: InternetAddress, logger: logging.Logger = logging.getLogger("PyRakLib"),
                 max_mtu_size: int = 1492, override_protocol_version: int = None):
        super().__init__()
        self.address = address
        self.server_id = random.randint(0, sys.maxsize)
        self.max_mtu_size = max_mtu_size
        self.logger = logger
        self.internal_queue = queue.LifoQueue()
        self.external_queue = queue.LifoQueue()
        self.protocol_version = override_protocol_version or PyRakLib.DEFAULT_PROTOCOL_VERSION
        if address.port < 1 or address.port > 65536:
            raise ValueError("Invalid port range")
        self.main_path = os.getcwd()
        self.start()

    def is_shutdown(self) -> bool:
        return self._shutdown is True

    def shutdown(self):
        self._shutdown = True

    def get_server_id(self):
        return self.server_id

    def get_protocol_version(self):
        return self.protocol_version

    def get_logger(self):
        return self.logger

    def get_external_queue(self):
        return self.external_queue

    def get_internal_queue(self):
        return self.internal_queue

    def push_main_to_thread_packet(self, pkt: bytes):
        self.internal_queue.put(pkt)

    def read_main_to_thread_packet(self) -> bytes:
        if self.internal_queue.empty():
            return b""
        return self.internal_queue.get()

    def push_thread_to_main_packet(self, pkt: bytes):
        self.external_queue.put(pkt)

    def read_thread_to_main_packet(self) -> bytes:
        if self.external_queue.empty():
            return b""
        return self.external_queue.get()

    def shutdown_handler(self):
        if self._shutdown is not True:
            self.logger.error("PyRakLib Thread [#" + str(self.ident) + "] crashed.")

    def run(self):
        gc.enable()
        atexit.register(self.shutdown_handler)
        socket = UDPServerSocket(self.address)
        SessionManager(self, socket, self.max_mtu_size)

    def __str__(self):
        print("INTERNAL QUEUE:")
        print(self.internal_queue.get())
        print("EXTERNAL QUEUE:")
        print(self.external_queue.get())
        return "(PyRakLibServer)" + \
               "ADDRESS: " + self.address.__str__() + \
               "SERVER_ID: " + str(self.server_id) + \
               "MAIN_PATH: " + self.main_path + \
               "MAX_MTU_SIZE: " + str(self.max_mtu_size) + \
               "PROTOCOL_VERSION: " + str(self.protocol_version) + \
               "SHUTDOWN: " + str(self._shutdown)
