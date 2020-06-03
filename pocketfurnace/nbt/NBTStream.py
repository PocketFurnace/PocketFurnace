from pocketfurnace.nbt.NBT import NBT
from pocketfurnace.nbt.ReaderTracker import ReaderTracker
import zlib
import abc
from pocketfurnace.nbt.tag.NamedTag import NamedTag
from pocketfurnace.utils.Binary import Binary


class NBTStream(metaclass=abc.ABCMeta):
    buffer = ""
    offset = 0

    def get(self, length) -> str:
        if length == 0:
            return ""

        buflen = len(self.buffer)
        if length is True:
            string = self.buffer[self.offset:]
            self.offset = buflen
            return string
        if length < 0:
            self.offset = buflen - 1
            return ""

        remaining = buflen - self.offset
        if remaining < length:
            print("[PocketFurnace]: Not enough bytes left in buffer: need " + str(length) + ", have " + str(remaining))

        if length == 1:
            self.offset += 1
            return self.buffer[self.offset]
        else:
            self.offset += length
            return self.buffer[self.offset - length:self.offset + length]

    def put(self, v: str):
        self.buffer += v

    def feof(self) -> bool:
        return bool(self.offset not in self.buffer)

    # Decodes NBT from the given binary string and returns it.
    def read(self, buffer, doMultiple=False, offset=0, maxDepth=0):
        self.offset = offset
        self.buffer = buffer
        data = self.read_tag(ReaderTracker(maxDepth))

        if data is None:
            print("[PocketFurnace]: Found TAG_End at the start of buffer")

        if doMultiple and not self.feof():
            data = [data]
            # help me DIEGO!!!!!!!!!!!!

    # Decodes NBT from the given compressed binary string and returns it. Anything decodable by zlib_decode() can be
    # processed
    def read_compressed(self, buffer: str):
        buffer = buffer if isinstance(buffer, bytes) else buffer.encode('utf-8')
        return self.read(zlib.decompress(buffer))

    def write(self, data):
        pass  # help me DIEGO!!!!!!!!!!!!

    def write_compressed(self, data, compression=31, level=7):
        pass  # help me DIEGO!!!!!!!!!!!!

    def read_tag(self, tracker: ReaderTracker):
        tagType = self.get_byte()
        if tagType == NBT.TAG_End:
            return None

        tag = NBT.createTag(tagType)
        tag.setName(self.get_string())
        tag.read(self, tracker)

    def write_tag(self, tag: NamedTag):
        pass  # help me DIEGO!!!!!!!!!!!!

    def write_end(self):
        self.put_byte(NBT.TAG_End)

    def get_byte(self) -> int:
        return Binary.read_byte(bytes(self.get(1)))

    def get_signed_byte(self) -> int:
        return Binary.read_signed_byte(bytes(self.get(1)))

    def put_byte(self, v: int):
        self.buffer += Binary.write_byte(v)

    @abc.abstractmethod
    def get_short(self) -> int:
        pass

    @abc.abstractmethod
    def get_signed_short(self) -> int:
        pass

    @abc.abstractmethod
    def put_short(self, v: int):
        pass

    @abc.abstractmethod
    def get_int(self) -> int:
        pass

    @abc.abstractmethod
    def put_int(self, v: int):
        pass

    @abc.abstractmethod
    def get_long(self) -> int:
        pass

    @abc.abstractmethod
    def put_long(self, v: int):
        pass

    @abc.abstractmethod
    def get_float(self) -> float:
        pass

    @abc.abstractmethod
    def put_float(self, v: float):
        pass

    @abc.abstractmethod
    def get_double(self) -> float:
        pass

    @abc.abstractmethod
    def put_double(self, v: float):
        pass

    def get_string(self) -> str:
        return self.get(NBTStream.check_read_string_length(self.get_short()))

    def put_string(self, v: str):
        self.put_short(NBTStream.check_read_string_length(int(v)))
        self.put(v)

    @staticmethod
    def check_read_string_length(length: int) -> int:
        if length > 32767:
            print("[PocketFurnace]: NBT string length too large (length > 32767)")
        return length

    @staticmethod
    def check_write_string_length(length: int) -> int:
        if length > 32767:
            print("[PocketFurnace]: NBT string length too large (length > 32767)")
        return length

    @abc.abstractmethod
    def get_int_array(self):
        pass

    @abc.abstractmethod
    def put_int_array(self, array):
        pass

    @staticmethod
    def to_array(data):
        array = {}
        NBTStream.tag_to_array(array, data)
        return array

    @staticmethod
    def tag_to_array(data, tag: NamedTag):
        # help me DIEGO!!!!!!!!!!!!
        pass
