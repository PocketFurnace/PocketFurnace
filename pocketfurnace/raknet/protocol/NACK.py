from pocketfurnace.raknet.protocol.AcknowledgePacket import AcknowledgePacket


class NACK(AcknowledgePacket):
    ID = 0xa0
