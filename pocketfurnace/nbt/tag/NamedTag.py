from abc import ABCMeta, abstractmethod
from copy import deepcopy

from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker


class NamedTag:
    __metaclass__ = ABCMeta

    name = None
    cloning = False

    def __init__(self, name: str = ""):
        if len(name) > 32767:
            raise ValueError(f"Tag name cannot be more than 32767 bytes, got length {len(name)}")
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: bytes):
        self.name = name

    @abstractmethod
    def get_value(self): pass

    @abstractmethod
    def get_type(self) -> int: pass

    @abstractmethod
    def write(self, nbt: NBTStream): pass

    @abstractmethod
    def read(self, nbt: NBTStream, tracker: ReaderTracker): pass

    def to_string(self, indentation: int = 0):
        return ("  " * indentation) + self.__name__ + ": " + f"name={self.name}, " + f"value={str(self.get_value())}"

    def safe_clone(self):
        if self.cloning:
            raise RuntimeError("Recursive NBT tag dependency detected")
        self.cloning = True
        retval = deepcopy(self)
        self.cloning = False
        retval.cloning = False
        return retval

    def equals(self, that) -> bool:
        return self.name == that.name and self.equals_value(that)

    def equals_value(self, that) -> bool:
        return isinstance(that, self.__class__) and self.get_value() == that.get_value()

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_name(), self.get_value()
