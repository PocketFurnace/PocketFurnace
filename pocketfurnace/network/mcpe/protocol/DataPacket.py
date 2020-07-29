from pocketfurnace.network.mcpe.NetworkBinaryStream import NetworkBinaryStream


class DataPacket(NetworkBinaryStream):
    NID = 0
    PID_MASK = 0x3ff  # 10 Bits

    SUBCLIENT_ID_MASK = 0x03  # 2 Bits
    SENDER_SUBCLIENT_ID_SHIFT = 10
    RECIPIENT_SUBCLIENT_ID_SHIFT = 12

    isEncoded = False
    _encapsulatedPacket = None

    senderSubId = 0
    recipientSubId = 0

    def pid(self):
        return self.NID

    def get_name(self):
        return type(object).__name__

    def can_be_batched(self):
        return True

    def can_be_sent_before_login(self):
        return False

    def may_have_unread_bytes(self):
        return False

    def decode_payload(self): pass

    def decode(self):
        self.offset = 0
        self.decodeHeader()
        self.decode_payload()

    def decodeHeader(self):
        header = self.get_unsigned_var_int()
        pid = header & self.PID_MASK
        if pid != self.NID:
            raise Exception("Expected " + str(self.NID) + " for packet ID, got " + str(pid))
        self.senderSubId = (header >> self.SENDER_SUBCLIENT_ID_SHIFT) & self.SUBCLIENT_ID_MASK
        self.recipientSubId = (header >> self.RECIPIENT_SUBCLIENT_ID_SHIFT) & self.SUBCLIENT_ID_MASK

    def encode_payload(self): pass

    def encode(self):
        self.reset()
        self.encode_header()
        self.encode_payload()
        self.isEncoded = True

    def encode_header(self):
        self.put_unsigned_var_int(
            self.NID |
            (self.senderSubId << self.SENDER_SUBCLIENT_ID_SHIFT) |
            (self.recipientSubId << self.RECIPIENT_SUBCLIENT_ID_SHIFT)
        )

    def write_payload(self): pass

    def clean(self):
        self.buffer = ""
        self.isEncoded = False
        self.offset = 0
        return self
