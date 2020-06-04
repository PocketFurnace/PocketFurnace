from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class FloatTag(NamedTag):
    value = 0.0

    def __init__(self, name: str = "", value: float = 0.0):
        super().__init__(name)
        self.value = value

    def get_type(self) -> int:
        return NBT.TAG_Float

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = nbt.get_float()

    def write(self, nbt: NBTStream):
        nbt.put_float(self.value)

    def get_value(self) -> float:
        return self.value
