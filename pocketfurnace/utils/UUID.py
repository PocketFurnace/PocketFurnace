import hashlib
import os
import random
import time

from pocketfurnace.utils.Binary import Binary
from pocketfurnace.utils.Utils import Utils


class UUID:
    parts = [0, 0, 0, 0]
    version = None

    def __init__(self, part1=0, part2=0, part3=0, part4=0, version=None):
        self.parts[0] = int(part1)
        self.parts[1] = int(part2)
        self.parts[2] = int(part3)
        self.parts[3] = int(part4)
        self.version = (self.parts[1] & 0xf000) >> 12 if version == None else int(version)

    def get_version(self):
        return self.version

    def equals(self, uuid):
        return uuid.parts[0] == self.parts[0] and uuid.parts[1] == self.parts[1] and uuid.parts[2] == self.parts[2] and \
               uuid.parts[3] == self.parts[3]

    def from_binary(self, uuid, version=None):
        if len(uuid) != 16:
            raise Exception("Must have exactly 16 bytes")
        return UUID(Binary.read_int(Utils.substr(uuid, 0, 4)), Binary.read_int(Utils.substr(uuid, 4, 4)),
                    Binary.read_int(Utils.substr(uuid, 8, 4)), Binary.read_int(Utils.substr(uuid, 12, 4)), version)

    def from_string(self, uuid, version=None):
        return self.from_binary(Utils.hex2bin(uuid.strip().replace("-", "")), version)

    def from_data(self, data):
        hash = hashlib.new("md5").update("".join(data))
        return self.from_binary(hash, 3)

    def from_random(self):
        return self.from_data(Binary.write_int(int(time.time())), Binary.write_short(os.getpid()),
                             Binary.write_short(os.geteuid()), Binary.write_int(random.randint(-0x7fffffff, 0x7fffffff)),
                             Binary.write_int(random.randint(-0x7fffffff, 0x7fffffff)))

    def to_binary(self):
        return Binary.write_int(self.parts[0]) + Binary.write_int(self.parts[1]) + Binary.write_int(
            self.parts[2]) + Binary.write_int(self.parts[3])

    def to_string(self):
        hex = Utils.hex2bin(self.to_binary())
        if self.version != None:
            return Utils.substr(hex, 0, 8) + "-" + Utils.substr(hex, 8, 4) + "-" + int(self.version, 16) + Utils.substr(
                hex, 13, 3) + "-8" + Utils.substr(hex, 17, 3) + "-" + Utils.substr(hex, 20, 12)
        return Utils.substr(hex, 0, 8) + "-" + Utils.substr(hex, 8, 4) + "-" + Utils.substr(hex, 12,
                                                                                            4) + "-" + Utils.substr(hex,
                                                                                                                    16,
                                                                                                                    4) + "-" + Utils.substr(
            hex, 20, 12)

    def get_part(self, part_number: int):
        if part_number < 0 or part_number > 3:
            raise Exception("Invalid UUID part index" + str(part_number))
        return self.parts[part_number]