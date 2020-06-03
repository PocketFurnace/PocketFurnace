from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class ByteArrayTag(NamedTag):
    value = ""

    def __init__(self, name: str = "", value: str = ""):
        super().__init__(name)
        self.value = value

    def get_type(self) -> int:
        return NBT.TAG_ByteArray

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = nbt.get(nbt.get_int())

    def write(self, nbt: NBTStream):
        nbt.put_int(len(self.value))
        nbt.put(bytes(self.value))

    def get_value(self) -> str:
        return self.value
