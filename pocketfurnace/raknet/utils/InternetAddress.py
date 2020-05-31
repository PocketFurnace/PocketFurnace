
class InternetAddress:
    ip = None
    port = None
    version = None

    def __init__(self, ip: str, port: int, version: int):
        self.ip = ip
        if port < 0 or port > 65535:
            raise TypeError("Invalid UDP Port range")
        self.port = port
        self.version = version

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_version(self):
        return self.version

    def to_string(self):
        return self.ip + ":" + str(self.port)

    def equals(self, address) -> bool:
        if isinstance(address, self.__class__):
            return address.ip == self.ip and address.port == self.port and address.version == self.version

    def __str__(self):
        return "(InternetAddress) IP: " + self.ip + " PORT: " + str(self.port) + " VERSION: " + str(self.version)
