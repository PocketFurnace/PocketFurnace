from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class ShortTag(NamedTag):
    value = 0

    def __init__(self, name: str = "", value: int = 0):
        super().__init__(name)
        if value < -0x8000 or value > 0x7fff:
            print("Value "+str(value)+" is too large!")
        self.value = value

    def get_type(self) -> int:
        return NBT.TAG_Short

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = nbt.get_signed_short()

    def write(self, nbt: NBTStream):
        nbt.put_short(self.value)

    def get_value(self) -> int:
        return self.value
