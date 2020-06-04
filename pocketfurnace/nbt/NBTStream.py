import ast
import numbers
from abc import ABCMeta, abstractmethod
from gzip import compress, decompress

from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
from pocketfurnace.nbt.tag.ByteTag import ByteTag
from pocketfurnace.nbt.tag.CompoundTag import CompoundTag
from pocketfurnace.nbt.tag.FloatTag import FloatTag
from pocketfurnace.nbt.tag.IntArrayTag import IntArrayTag
from pocketfurnace.nbt.tag.IntTag import IntTag
from pocketfurnace.nbt.tag.ListTag import ListTag
from pocketfurnace.nbt.tag.NamedTag import NamedTag
from pocketfurnace.nbt.tag.StringTag import StringTag
from pocketfurnace.utils.Binary import Binary


def is_numeric(obj):
    if isinstance(obj, numbers.Number):
        return True
    elif isinstance(obj, str):
        nodes = list(ast.walk(ast.parse(obj)))[1:]
        if not isinstance(nodes[0], ast.Expr):
            return False
        if not isinstance(nodes[-1], ast.Num):
            return False
        nodes = nodes[1:-1]
        for i in range(len(nodes)):
            if i % 2 == 0:
                if not isinstance(nodes[i], ast.UnaryOp):
                    return False
            else:
                if not isinstance(nodes[i], (ast.USub, ast.UAdd)):
                    return False
        return True
    else:
        return False


class NBTStream(metaclass=ABCMeta):
    buffer = b""
    offset = 0

    def get(self, length) -> bytes:
        if length < 0:
            return b""
        elif isinstance(length, bool) and length:
            return self.buffer[0:self.offset]
        else:
            buffer = self.buffer[self.offset:self.offset + length]
            self.offset += length
            return buffer

    def put(self, v: bytes):
        self.buffer += v

    def feof(self) -> bool:
        try:
            self.buffer[self.offset]
        except(KeyError, IndexError):
            return False
        return True

    # Decodes NBT from the given binary string and returns it.
    def read(self, buffer: bytes, do_multiple: bool = False, offset: int = 0, max_depth: int = 0):
        self.offset = offset
        self.buffer = buffer
        data = self.read_tag(ReaderTracker(max_depth))

        if data is None:
            print("[PocketFurnace]: Found TAG_End at the start of buffer")

        if do_multiple and not self.feof():
            data = [data]
            while True:
                tag = self.read_tag(ReaderTracker(max_depth))
                if tag is not None:
                    data.append(tag)
                if not self.feof():
                    break
        self.buffer = b""
        return data

    # Decodes NBT from the given compressed binary string and returns it. Anything decodable by zlib_decode() can be
    # processed
    def read_compressed(self, buffer: bytes):
        return self.read(decompress(buffer))

    def write(self, data):
        self.offset = 0
        self.buffer = b""

        if isinstance(data, NamedTag):
            self.write_tag(data)
            return self.buffer
        elif isinstance(data, list):
            for tag in data:
                self.write_tag(tag)
            return self.buffer
        return False

    def write_compressed(self, data, level: int = 7):
        write = self.write(data)
        if write is not False:
            return compress(data, level)
        return False

    def read_tag(self, tracker: ReaderTracker):
        tag_type = self.get_byte()
        if tag_type == NBT.TAG_End:
            return None

        tag = NBT.create_tag(tag_type)
        tag.set_name(self.get_string())
        tag.read(self, tracker)
        return tag

    def write_tag(self, tag: NamedTag):
        self.put_byte(tag.get_type())
        self.put_string(tag.get_name())
        tag.write(self)

    def write_end(self):
        self.put_byte(NBT.TAG_End)

    def get_byte(self) -> int:
        return Binary.read_byte(bytes(self.get(1)))

    def get_signed_byte(self) -> int:
        return Binary.read_signed_byte(bytes(self.get(1)))

    def put_byte(self, v: int):
        self.buffer += Binary.write_byte(v)

    @abstractmethod
    def get_short(self) -> int: pass

    @abstractmethod
    def get_signed_short(self) -> int: pass

    @abstractmethod
    def put_short(self, v: int): pass

    @abstractmethod
    def get_int(self) -> int: pass

    @abstractmethod
    def put_int(self, v: int): pass

    @abstractmethod
    def get_long(self) -> int: pass

    @abstractmethod
    def put_long(self, v: int): pass

    @abstractmethod
    def get_float(self) -> float: pass

    @abstractmethod
    def put_float(self, v: float): pass

    @abstractmethod
    def get_double(self) -> float: pass

    @abstractmethod
    def put_double(self, v: float): pass

    def get_string(self) -> bytes:
        return self.get(self.check_read_string_length(self.get_short()))

    def put_string(self, v: str):
        self.put_short(NBTStream.check_read_string_length(int(v)))
        self.put(v.encode("UTF-8"))

    @staticmethod
    def check_read_string_length(length: int) -> int:
        if length > 32767:
            raise ValueError(f"[PocketFurnace]: NBT string length too large ({length} > 32767)")
        return length

    @staticmethod
    def check_write_string_length(length: int) -> int:
        if length > 32767:
            raise TypeError(f"[PocketFurnace]: NBT string length too large ({length} > 32767)")
        return length

    @abstractmethod
    def get_int_array(self): pass

    @abstractmethod
    def put_int_array(self, array): pass

    @staticmethod
    def to_array(data):
        array = {}
        NBTStream.tag_to_array(array, data)
        return array

    @staticmethod
    def tag_to_array(data: dict, tag: NamedTag):
        for (k, v) in tag:
            if isinstance(v, CompoundTag) or isinstance(v, ListTag) or isinstance(v, IntArrayTag):
                data.update({k: []})
                NBTStream.tag_to_array(data[k], v)
            else:
                data.update({k: v.get_value()})

    @staticmethod
    def from_array_guesser(key: str, value):
        if isinstance(value, int):
            return IntTag(key, value)
        elif isinstance(value, float):
            return FloatTag(key, value)
        elif isinstance(key, str):
            return StringTag(key, value)
        elif isinstance(key, bool):
            return ByteTag(key, value)
        return None

    @staticmethod
    def tag_from_array(tag: NamedTag, data: dict, guesser):
        """
        :param tag:
        :param data:
        :param guesser:
        :type guesser: callable
        """
        for (k, v) in data:
            if isinstance(v, dict):
                _is_numeric = True
                _is_int_array = True
                for (key, value) in v:
                    if not is_numeric(key):
                        _is_numeric = False
                        break
                    elif not isinstance(value, int):
                        _is_int_array = False
                if _is_numeric:
                    if _is_int_array:
                        tag.key = IntArrayTag(k, {})
                    else:
                        tag.key = ListTag(k, {})
                else:
                    tag.key = CompoundTag(k, {})
            else:
                v = guesser(k, v)
                if isinstance(v, NamedTag):
                    tag.key = v

    @staticmethod
    def from_array(data: dict, guesser=None):
        tag = CompoundTag("", {})
        NBTStream.tag_from_array(tag, data, guesser or eval(NBTStream.from_array_guesser.__name__))
        return tag
