from pocketfurnace.nbt.tag.NamedTag import NamedTag


class NBT:
    TAG_End = 0
    TAG_Byte = 1
    TAG_Short = 2
    TAG_Int = 3
    TAG_Long = 4
    TAG_Float = 5
    TAG_Double = 6
    TAG_ByteArray = 7
    TAG_String = 8
    TAG_List = 9
    TAG_Compound = 10
    TAG_IntArray = 11

    @staticmethod
    def createTag(type: int) -> NamedTag:
        if type == NBT.TAG_Byte:
            pass
        if type == NBT.TAG_Short:
            pass
        if type == NBT.TAG_Int:
            pass
        if type == NBT.TAG_Long:
            pass
        if type == NBT.TAG_Float:
            pass
        if type == NBT.TAG_Double:
            pass
        if type == NBT.TAG_ByteArray:
            pass
        if type == NBT.TAG_String:
            pass
        if type == NBT.TAG_List:
            pass
        if type == NBT.TAG_Compound:
            pass
        if type == NBT.TAG_IntArray:
            pass
