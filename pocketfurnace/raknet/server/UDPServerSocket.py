import socket

from pocketfurnace.raknet.utils.InternetAddress import InternetAddress


class UDPServerSocket:
    socket = None
    _bind_address = None

    def __init__(self, bind_address: InternetAddress):
        self._bind_address = bind_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            # TODO: Add IPv6 support
            self.socket.bind((bind_address.get_ip(), bind_address.get_port()))
        except Exception as e:
            print("FAILED TO BIND TO PORT! Perhaps another server is running on the port?")
            print(str(e))
        finally:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.socket.setblocking(False)  # Non-blocking

    def close(self):
        self.socket.close()

    def get_bind_address(self):
        return self._bind_address

    def get_socket(self):
        return self.socket

    @staticmethod
    def get_last_error():
        return socket.error.strerror

    def read_packet(self):
        try:
            data = self.socket.recvfrom(65535)
            # print("Packet IN: "+str(data))
            return data
        except socket.error:
            pass

    def write_packet(self, buffer, dest, port):
        # print("Packet OUT: "+str(buffer))
        return self.socket.sendto(buffer, (dest, port))

    def set_send_buffer(self, size: int):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, size)
        return self

    def set_recv_buffer(self, size: int):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)
        return self
