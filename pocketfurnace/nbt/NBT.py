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
    def create_tag(_type: int) -> NamedTag:
        if _type == NBT.TAG_Byte:
            pass
        elif _type == NBT.TAG_Short:
            pass
        elif _type == NBT.TAG_Int:
            pass
        elif _type == NBT.TAG_Long:
            pass
        elif _type == NBT.TAG_Float:
            pass
        elif _type == NBT.TAG_Double:
            pass
        elif _type == NBT.TAG_ByteArray:
            pass
        elif _type == NBT.TAG_String:
            pass
        elif _type == NBT.TAG_List:
            pass
        elif _type == NBT.TAG_Compound:
            pass
        elif _type == NBT.TAG_IntArray:
            pass
        else:
            raise ValueError(f"Unknown NBT tag type {_type}")
