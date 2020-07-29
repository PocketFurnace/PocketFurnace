from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo
from pocketfurnace.network.mcpe.protocol.types.PlayerPermissions import PlayerPermissions


class AdventureSettingsPacket(DataPacket):
    NID = ProtocolInfo.ADVENTURE_SETTINGS_PACKET

    PERMISSION_NORMAL = 0
    PERMISSION_OPERATOR = 1
    PERMISSION_HOST = 2
    PERMISSION_AUTOMATION = 3
    PERMISSION_ADMIN = 4

    BITFLAG_SECOND_SET = 1 << 16

    WORLD_IMMUTABLE = 0x01
    NO_PVP = 0x02

    AUTO_JUMP = 0x20
    ALLOW_FLIGHT = 0x40
    NO_CLIP = 0x80
    WORLD_BUILDER = 0x100
    FLYING = 0x200
    MUTED = 0x400

    BUILD_AND_MINE = 0x01 | BITFLAG_SECOND_SET
    DOORS_AND_SWITCHES = 0x02 | BITFLAG_SECOND_SET
    OPEN_CONTAINERS = 0x04 | BITFLAG_SECOND_SET
    ATTACK_PLAYERS = 0x08 | BITFLAG_SECOND_SET
    ATTACK_MOBS = 0x10 | BITFLAG_SECOND_SET
    OPERATOR = 0x20 | BITFLAG_SECOND_SET
    TELEPORT = 0x80 | BITFLAG_SECOND_SET

    flags = 0
    commandPermission = PERMISSION_NORMAL
    flags2 = -1
    playerPermission = PlayerPermissions.MEMBER
    customFlags = 0
    entityUniqueId = None

    def decode_payload(self):
        self.flags = self.put_unsigned_var_int()
        self.commandPermission = self.put_unsigned_var_int()
        self.flags2 = self.put_unsigned_var_int()
        self.playerPermission = self.put_unsigned_var_int()
        self.customFlags = self.put_unsigned_var_int()
        self.entityUniqueId = self.get_l_long()

    def encode_payload(self):
        self.put_unsigned_var_int(self.flags)
        self.put_unsigned_var_int(self.commandPermission)
        self.put_unsigned_var_int(self.flags2)
        self.put_unsigned_var_int(self.playerPermission)
        self.put_unsigned_var_int(self.customFlags)
        self.put_l_long(self.entityUniqueId)

    def get_flag(self, flag):
        if (flag & self.BITFLAG_SECOND_SET) != 0:
            return (self.flags2 & flag) != 0

        return (self.flags & flag) != 0

    def set_flag(self, flag, value):
        if (flag & self.BITFLAG_SECOND_SET) != 0:
            flagSet = self.flags2
        else:
            flagSet = self.flag

        if value:
            flagSet |= flag
        else:
            flagSet &= ~flag