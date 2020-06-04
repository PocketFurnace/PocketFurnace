import copy
from typing import Dict, AnyStr

from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.ByteArrayTag import ByteArrayTag
from pocketfurnace.nbt.tag.ByteTag import ByteTag
from pocketfurnace.nbt.tag.DoubleTag import DoubleTag
from pocketfurnace.nbt.tag.FloatTag import FloatTag
from pocketfurnace.nbt.tag.IntArrayTag import IntArrayTag
from pocketfurnace.nbt.tag.IntTag import IntTag
from pocketfurnace.nbt.tag.ListTag import ListTag
from pocketfurnace.nbt.tag.LongTag import LongTag
from pocketfurnace.nbt.tag.NamedTag import NamedTag
from pocketfurnace.nbt.tag.ShortTag import ShortTag
from pocketfurnace.nbt.tag.StringTag import StringTag


class CompoundTag(NamedTag):

    value: Dict[AnyStr, NamedTag] = {}

    def __init__(self, name: str = "", value: dict = None):
        super().__init__(name)
        for tag in value:
            self.set_tag(tag)

    def count(self) -> int:
        return len(self.value)

    def get_count(self) -> int:
        return len(self.value)

    def get_value(self):
        return self.value

    # Returns the tag with the specified name, or null if it does not exist.
    def get_tag(self, name: str, expected_class=NamedTag.__class__):
        assert isinstance(expected_class, NamedTag.__class__)
        tag = self.value[name]
        if tag is not None and not isinstance(tag, expected_class.__class__):
            raise RuntimeError(f"Expected a tag of type {expected_class.__class__}, got {tag.__class__}")
        return tag

    # Returns the ListTag with the specified name, or null if it does not exist. Triggers an exception if a tag exists
    # with that name and the tag is not a ListTag
    def get_list_tag(self, name: str):
        return self.get_tag(name, ListTag.__class__)

    # Returns the CompoundTag with the specified name, or null if it does not exist. Triggers an exception if a tag
    # exists with that name and the tag is not a CompoundTag.
    def get_compound_tag(self, name: str):
        return self.get_tag(name, CompoundTag.__class__)

    # Sets the specified NamedTag as a child tag of the CompoundTag at the offset specified by the tag's name. If a tag
    # already exists at the offset and the types do not match, an exception will be thrown unless $force is true.
    def set_tag(self, tag: NamedTag, force: bool = False):
        if not force:
            existing = self.value[tag.name] or None
            if existing is not None and not isinstance(tag, existing.__class__):
                raise RuntimeError(f"Cannot set tag at {tag.name}: tried to overwrite {existing.__name__} with {tag.__class__.__name__}")
        else:
            self.value[tag.name] = tag

    # Removes the child tags with the specified names from the CompoundTag. This function accepts a variadic list of
    # strings
    def remove_tag(self, *names: str):
        for name in names:
            del self.value[name]

    # Returns whether the CompoundTag contains a child tag with the specified name
    def has_tag(self, name: str, expected_class=NamedTag.__class__) -> bool:
        assert isinstance(expected_class, NamedTag.__class__)
        if name in self.value and isinstance(name, expected_class.__class__):
            return True
        else:
            return False

    # Returns the value of the child tag with the specified name, or $default if the tag doesn't exist. If the child
    # tag is not of type $expectedType, an exception will be thrown, unless a default is given and $bad_tag_default is
    # true
    def get_tag_value(self, name: str, expected_class=NamedTag.__class__, default=None, bad_tag_default: bool = False):
        tag: NamedTag = self.get_tag(name, NamedTag.__class__ if bad_tag_default else expected_class.__class__)

        if isinstance(tag, expected_class.__class__):
            return tag.get_value()

        if default is None:
            raise RuntimeError(f"Tag with name {name} {'not of expecting type' if tag is not None else 'not found'} and no valid default value given")
        return default

    def get_byte(self, name: str, default: int = None, bad_tag_default: bool = False) -> int:
        return self.get_tag_value(name, ByteTag.__class__, default, bad_tag_default)

    def get_short(self, name: str, default: int = None, bad_tag_default: bool = False) -> int:
        return self.get_tag_value(name, ShortTag.__class__, default, bad_tag_default)

    def get_int(self, name: str, default: int = None, bad_tag_default: bool = False) -> int:
        return self.get_tag_value(name, IntTag.__class__, default, bad_tag_default)

    def get_long(self, name: str, default: int = None, bad_tag_default: bool = False) -> int:
        return self.get_tag_value(name, LongTag.__class__, default, bad_tag_default)

    def get_float(self, name: str, default: int = None, bad_tag_default: bool = False) -> int:
        return self.get_tag_value(name, FloatTag.__class__, default, bad_tag_default)

    def get_double(self, name: str, default: int = None, bad_tag_default: bool = False) -> int:
        return self.get_tag_value(name, DoubleTag.__class__, default, bad_tag_default)

    def get_byte_array(self, name: str, default: int = None, bad_tag_default: bool = False) -> bytearray:
        return self.get_tag_value(name, ByteArrayTag.__class__, default, bad_tag_default)

    def get_string(self, name: str, default: int = None, bad_tag_default: bool = False) -> str:
        return self.get_tag_value(name, StringTag.__class__, default, bad_tag_default)

    def get_int_array(self, name: str, default: int = None, bad_tag_default: bool = False) -> list:
        return self.get_tag_value(name, IntArrayTag.__class__, default, bad_tag_default)

    def set_byte(self, name: str, value: int, force: bool = False):
        self.set_tag(ByteTag(name, value), force)

    def set_short(self, name: str, value: int, force: bool = False):
        self.set_tag(ShortTag(name, value), force)

    def set_int(self, name: str, value: int, force: bool = False):
        self.set_tag(IntTag(name, value), force)

    def set_long(self, name: str, value: int, force: bool = False):
        self.set_tag(LongTag(name, value), force)

    def set_float(self, name: str, value: float, force: bool = False):
        self.set_tag(FloatTag(name, value), force)

    def set_double(self, name: str, value: float, force: bool = False):
        self.set_tag(DoubleTag(name, value), force)

    def set_bytearray(self, name: str, value: str, force: bool = False):
        self.set_tag(ByteArrayTag(name, value), force)

    def set_string(self, name: str, value: str, force: bool = False):
        self.set_tag(StringTag(name, value), force)

    def set_int_array(self, name: str, value: list, force: bool = False):
        self.set_tag(IntArrayTag(name, value), force)

    def offset_exists(self, offset):
        return offset in self.value

    def offset_get(self, offset):
        if offset in self.value:
            if isinstance(self.value[offset], list):
                return self.value[offset]
            else:
                return self.value[offset].get_value()
        assert(False, f"Offset {offset} not found")
        return None

    def offset_set(self, offset, value):
        if offset is None:
            raise ValueError("List access push syntax is not supported")
        if isinstance(value, NamedTag):
            if offset != value.get_name():
                raise ValueError(f"Given tag has a name which does not match th offset given (offser: {offset}, tag name: {value.get_name()})")
            self.value[offset] = value
        else:
            raise TypeError(f"Value set by ListAccess must be an instance of {NamedTag.__name__}")

    def offset_unset(self, offset):
        del self.value[offset]

    def get_type(self) -> int:
        return NBT.TAG_Compound

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        self.value = {}

        def internal():
            while True:
                tag = nbt.read_tag(tracker)
                if tag is not None:
                    if tag.name in self.value:
                        raise ValueError(f"Duplicate key {tag.name}")
                    self.value[tag.name] = tag
                if tag is None:
                    break
        tracker.protect_depth(internal())

    def write(self, nbt: NBTStream):
        for tag in self.value:
            nbt.write_tag(tag)
        nbt.write_end()

    def to_string(self, indentation: int = 0):
        string = "  " * indentation + __name__ + f": name={self.name}, value=\n"
        for tag in self.value:
            string += tag.to_string(indentation + 1) + "\n"
        return string + ("  " * indentation) + "}"

    def clone(self):
        tag: NamedTag
        for(key, tag) in enumerate(self.value):
            self.value[key] = tag.safe_clone()

    def next_(self):
        next(self.value)

    def valid(self) -> bool:
        # TODO: This function will be a headache
        pass

    def key(self) -> str:
        # TODO: This function will be a headache
        pass

    def current(self):
        # TODO: This function will be a headache
        pass

    def equals_value(self, that) -> bool:
        if not (isinstance(that, self.__class__) or self.count() != that.count()):
            return False
        for (k, v) in self:
            other = that.get_tag(k)
            if other is None or not v.equals(other):
                return False

        return True

    def merge(self, other):
        new = copy.deepcopy(self)
        for named_tag in other:
            new.set_tag(copy.copy(named_tag))
        return new
