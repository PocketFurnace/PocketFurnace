from pocketfurnace.utils.Binary import Binary
from pocketfurnace.raknet.protocol.Packet import Packet


class AcknowledgePacket(Packet):
    RECORD_TYPE_RANGE = 0
    RECORD_TYPE_SINGLE = 1
    packets = []

    def _encodePayload(self) -> None:
        payload = ""
        self.packets.sort()
        count = len(self.packets)
        records = 0

        if count > 0:
            pointer = 1
            start = self.packets[0]
            last = self.packets[0]

            while pointer < count:
                current = self.packets[pointer + 1]
                diff = current - last
                if diff == 1:
                    last = current
                elif diff > 1:
                    if start is last:
                        payload += chr(self.RECORD_TYPE_SINGLE)
                        payload += Binary.write_l_triad(start)
                        start = last = current
                    else:
                        payload += chr(self.RECORD_TYPE_RANGE)
                        payload += Binary.write_l_triad(start)
                        payload += Binary.write_l_triad(last)
                        start = last = current

                    records += 1

            if start is last:
                payload += chr(self.RECORD_TYPE_SINGLE)
                payload += Binary.write_l_triad(start)
            else:
                payload += chr(self.RECORD_TYPE_RANGE)
                payload += Binary.write_l_triad(start)
                payload += Binary.write_l_triad(last)

            records += 1
            self.put_short(records)
            self.buffer += payload

            if start == last:
                payload += chr(self.RECORD_TYPE_SINGLE)
                payload += (Binary.write_l_triad(start))
            else:
                payload += chr(self.RECORD_TYPE_RANGE)
                payload += (Binary.write_l_triad(start))
                payload += (Binary.write_l_triad(last))
            records += 1
        self.put_short(records)
        self.buffer += payload

    def _decodePayload(self) -> None:
        self.get()
        count = self.get_short()
        self.packets = []
        cnt = 0
        i = 0
        while i < count and not self.feof() and cnt < 4096:
            if self.get_byte() == self.RECORD_TYPE_RANGE:
                start = self.get_l_triad()
                end = self.get_l_triad()
                if (end - start) > 512:
                    end = start + 512
                c = start
                while c == end or c < end:
                    cnt += 1
                    self.packets[cnt] = c
                    c += 1
            else:
                cnt += 1
                self.packets[cnt] = self.get_l_triad()
            i += 1

    def clean(self):
        super().clean()
        self.packets = []
