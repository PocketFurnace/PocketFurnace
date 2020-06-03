from pocketfurnace.nbt.NBTStream import NBTStream
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.ListTag import ListTag
from pocketfurnace.nbt.tag.NamedTag import NamedTag


class CompoundTag(NamedTag):
    value = {}

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
    def get_tag(self, name: str, expectedClass: type = NamedTag.__class__):
        assert isinstance(expectedClass, NamedTag.__class__)
        tag = self.value[name]
        if tag is not None and not isinstance(tag, expectedClass):
            print("Expected a tag of type")
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
            existing = None
            if tag.name in self.value:
                existing = self.value[tag.name]
            if existing is not None and not isinstance(tag, existing):
                print("Cannot set tag at " + tag.name)
        else:
            self.value[tag.name] = tag

    # Removes the child tags with the specified names from the CompoundTag. This function accepts a variadic list of
    # strings
    def remove_tag(self, names):
        for name in names:
            self.value[name].pop()

    # Returns whether the CompoundTag contains a child tag with the specified name
    def has_tag(self, name: str) -> bool:
        if name in self.value:
            return True
        else:
            return False





    def get_type(self) -> int:
        pass

    def write(self, nbt: NBTStream):
        pass

    def read(self, nbt: NBTStream, tracker: ReaderTracker):
        pass
