import abc

from pocketfurnace.network.mcpe.NetworkBinaryStream import NetworkBinaryStream


class DataPacket(metaclass=abc.ABCMeta, NetworkBinaryStream):
    NETWORK_ID = 0

    PID_MASK = 0x3ff

    SUB_CLIENT_ID_MASK = 0x03
    SENDER_SUB_CLIENT_ID_SHIFT = 10
    RECIPIENT_SUB_CLIENT_ID_SHIFT = 12

    is_encoded = False
    encapsulated_packet = None

    sender_sub_id = 0
    recipient_sub_id = 0

    def pid(self) -> int:
        return self.NETWORK_ID

    def get_name(self) -> str:
        return ""  # DIEGO CHECK THIS

    def can_be_batched(self) -> bool:
        return True

    def can_be_sent_before_login(self) -> bool:
        return False

    def may_have_unread_bytes(self) -> bool:
        return False

    def decode(self):
        self.offset = 0
        self.decode_header()
        self.decode_payload()

    def decode_header(self):
        header = self.get_unsigned_var_int()
        pid = header & self.PID_MASK
        if pid != self.NETWORK_ID:
            raise RuntimeError(f"Expected {self.NETWORK_ID} for packet ID, got {pid}")
        self.sender_sub_id = (header >> self.SENDER_SUB_CLIENT_ID_SHIFT) & self.SUB_CLIENT_ID_MASK
        self.recipient_sub_id = (header >> self.RECIPIENT_SUB_CLIENT_ID_SHIFT) & self.SUB_CLIENT_ID_MASK

    def decode_payload(self):
        pass

    def encode(self):
        self.reset()
        self.encode_header()
        self.encode_payload()
        self.is_encoded = True

    def encode_header(self):
        self.put_unsigned_var_int(self.NETWORK_ID |
                                  (self.sender_sub_id << self.SENDER_SUB_CLIENT_ID_SHIFT) |
                                  (self.recipient_sub_id << self.RECIPIENT_SUB_CLIENT_ID_SHIFT))

    def encode_payload(self):
        pass

    @abc.abstractmethod
    def handle(self, session) -> bool:  # instance NetworkSession soon
        pass

    def clean(self):
        self.buffer = 0
        self.is_encoded = False
        self.offset = 0
        return self

    def __debugInfo(self):
        pass  # DIEGO CHECK THIS

    def __get(self, name):
        pass  # DIEGO CHECK THIS

    def __set(self, name, value):
        pass  # DIEGO CHECK THIS
