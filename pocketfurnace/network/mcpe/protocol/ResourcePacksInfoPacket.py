from pocketfurnace.network.mcpe.protocol.DataPacket import DataPacket
from pocketfurnace.network.mcpe.protocol.ProtocolInfo import ProtocolInfo


class ResourcePacksInfoPacket(DataPacket):
    NID = ProtocolInfo.RESOURCE_PACKS_INFO_PACKET

    mustAccept = False
    hasScripts = False
    behaviorPackEntries = []
    resourcePackEntries = []

    def decode_payload(self):
        self.mustAccept = self.get_bool()
        self.hasScripts = self.get_bool()
        behaviorPackCount = self.get_short()
        while behaviorPackCount > 0:
            self.get_string()
            self.get_string()
            self.get_l_long()
            self.get_string()
            self.get_string()
            self.get_string()
            self.get_bool()
            behaviorPackCount -= 1

        resourcePackCount = self.get_l_short()
        while resourcePackCount > 0:
            self.get_string()
            self.get_string()
            self.get_l_long()
            self.get_string()
            self.get_string()
            self.get_string()
            self.get_bool()
            resourcePackCount -= 1

    def encode_payload(self):
        self.put_bool(self.mustAccept)
        self.put_bool(self.hasScripts)
        self.put_l_short(len(self.behaviorPackEntries))
        for entry in self.behaviorPackEntries:
            self.put_string(entry.getPackId())
            self.put_string(entry.getPackVersion())
            self.put_l_long(entry.getPackSize())
            self.put_string("")  # TODO: encryption key
            self.put_string("")  # TODO: subpack name
            self.put_string("")  # TODO: content identity
            self.put_bool(False)  # TODO: has scripts (?)

        self.put_l_short(len(self.resourcePackEntries))
        for entry in self.resourcePackEntries:
            self.put_string(entry.getPackId())
            self.put_string(entry.getPackVersion())
            self.put_l_long(entry.getPackSize())
            self.put_string("")  # TODO: encryption key
            self.put_string("")  # TODO: subpack name
            self.put_string("")  # TODO: content identity
            self.put_bool(False)  # TODO: seems useless for resource packs