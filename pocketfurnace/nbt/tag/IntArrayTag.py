from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class IntArrayTag(NamedTag):

    def __init__(self, name: str = "", value: dict = None):
        super().__init__(name)

    def get_value(self):
        pass

    def get_type(self) -> int:
        pass

    def write(self, nbt: NBTStream):
        pass

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        pass
