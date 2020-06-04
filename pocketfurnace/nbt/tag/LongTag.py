from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class LongTag(NamedTag):
    value = 0

    def __init__(self, name: str = "", value: int = 0):
        super().__init__(name)
        self.value = value

    def get_type(self) -> int:
        return NBT.TAG_Long

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = nbt.get_long()

    def write(self, nbt: NBTStream):
        nbt.put_long(self.value)

    def get_value(self) -> int:
        return self.value
