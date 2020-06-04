from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class StringTag(NamedTag):
    value = ""

    def __init__(self, name: str = "", value: str = ""):
        super().__init__(name)
        if len(value) > 32767:
            print("[PocketFurnace]: StringTag cannot hold more than 32767 bytes, got string of length "+str(len(value)))
        self.value = value

    def get_type(self) -> int:
        return NBT.TAG_String
    
    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = nbt.get_string()

    def write(self, nbt: NBTStream):
        nbt.put_string(self.value)

    def get_value(self) -> str:
        return self.value

