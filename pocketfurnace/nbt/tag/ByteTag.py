from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class ByteTag(NamedTag):

    value = 0

    def __init__(self, name: str = "", value: int = 0):
        super().__init__(name)
        if value < -128 or value > 127:
            print("Value "+str(value)+" is too large!")
        self.value = value

    def get_type(self) -> int:
        return NBT.TAG_Byte

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = nbt.get_signed_byte()

    def write(self, nbt: NBTStream):
        nbt.put_byte(self.value)

    def get_value(self) -> int:
        return self.value

