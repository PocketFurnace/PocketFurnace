from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.NamedTag import NamedTag


def _check(value: list):
    for v in value:
        if not isinstance(v, int):
            return False
        return True


class IntArrayTag(NamedTag):

    value = None

    def __init__(self, name: str = "", value: list = None):
        super().__init__(name)
        assert _check(value)
        self.value = value

    def get_value(self):
        return self.value

    def get_type(self) -> int:
        return NBT.TAG_IntArray

    def write(self, nbt: NBTStream):
        nbt.put_int_array(self.value)

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = nbt.get_int_array()

    def to_string(self, indentation: int = 0) -> str:
        return ("  " * indentation) + self.__name__ + ": " + f"name={self.name}, " + f"value=[{' '.join([str(i) for i in self.value])}]"
