from abc import ABCMeta


class PacketReliability:
    __metaclass__ = ABCMeta

    UNRELIABLE = 0
    UNRELIABLE_SEQUENCED = 1
    RELIABLE = 2
    RELIABLE_ORDERED = 3
    RELIABLE_SEQUENCED = 4
    UNRELIABLE_WITH_ACK_RECEIPT = 5
    RELIABLE_WITH_ACK_RECEIPT = 6
    RELIABLE_ORDERED_WITH_ACK_RECEIPT = 7

    @classmethod
    def is_reliable(cls, reliability: int) -> bool:
        return reliability == cls.RELIABLE or reliability == cls.RELIABLE_SEQUENCED or reliability == cls.RELIABLE_ORDERED or reliability == cls.RELIABLE_ORDERED_WITH_ACK_RECEIPT or reliability == cls.RELIABLE_WITH_ACK_RECEIPT

    @classmethod
    def is_sequenced(cls, reliability: int) -> bool:
        return reliability == cls.RELIABLE_SEQUENCED or reliability == cls.UNRELIABLE_SEQUENCED

    @classmethod
    def is_ordered(cls, reliability: int) -> bool:
        return reliability == cls.RELIABLE_ORDERED or reliability == cls.RELIABLE_ORDERED_WITH_ACK_RECEIPT

    @classmethod
    def is_sequenced_or_ordered(cls, reliability: int) -> bool:
        return reliability == cls.RELIABLE_SEQUENCED or reliability == cls.UNRELIABLE_SEQUENCED or reliability == cls.RELIABLE_ORDERED_WITH_ACK_RECEIPT or reliability == cls.UNRELIABLE_SEQUENCED
