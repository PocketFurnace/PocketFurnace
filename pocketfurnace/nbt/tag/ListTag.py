from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag
from pocketfurnace.nbt.tag.NoDynamicFieldsTrait import NoDynamicFieldsTrait
from pocketfurnace.nbt.utils.DoublyLinkedList import DoublyLinkedList


class ListTag(NamedTag, NoDynamicFieldsTrait):

    tag_type = None
    value = DoublyLinkedList()

    def __init__(self, name: str = "", value: dict = None, tag_type: int = NBT.TAG_End):
        super().__init__(name)
        self.tag_type = tag_type
        self.value = []

    def get_value(self):
        value = {}
        for (k, v) in self.value:
            value[k] = v
        return value

    def get_all_values(self):
        result = []
        for tag in self.value:
            if isinstance(tag, iter):
                result.append(tag)
            else:
                result.append(tag.get_value())
        return result

    def offset_exists(self, offset):
        return offset in self.value

    def offset_get(self, offset):
        value = self.value[offset] or None
        if isinstance(value, iter):
            return value
        elif value is not None:
            return value.get_value()
        return None

    def offset_set(self, offset, value):
        if isinstance(value, NamedTag):
            self.check_tag_type(value)
            self.value[offset] = value
        else:
            raise TypeError("Value set must be an instance of NamedTag")

    def offset_unset(self, offset):
        del self.value[offset]

    def count(self):
        return len(self.value)

    def push(self):
        pass

    def pop(self):
        pass

    def unshift(self):
        pass

    def shift(self):
        pass

    def insert(self):
        pass

    def remove(self):
        pass

    def get(self):
        pass

    def first(self):
        pass

    def last(self):
        pass

    def set(self):
        pass

    def isset(self, offset: int) -> bool:
        return offset in self.value

    def empty(self):
        pass

    def get_tag_type(self) -> int:
        return self.tag_type

    def set_tag_type(self, tag_type: int):
        pass

    def check_tag_type(self):
        pass

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        pass

    def write(self, nbt: NBTStream):
        pass

    def to_string(self, indentation: int = 0):
        pass

    def equals_value(self, that: NamedTag) -> bool:
        pass
