from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag
from pocketfurnace.nbt.tag.NoDynamicFieldsTrait import NoDynamicFieldsTrait


class ListTag(NamedTag, NoDynamicFieldsTrait):

    tag_type = None
    value = None

    def __init__(self, name: str = "", value: dict = None, tag_type: int = NBT.TAG_End):
        super().__init__(name)
        self.tag_type = tag_type
        self.value = []

    def get_value(self):
        pass

    def get_type(self) -> int:
        pass

    def write(self, nbt: NBTStream):
        pass

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        pass
