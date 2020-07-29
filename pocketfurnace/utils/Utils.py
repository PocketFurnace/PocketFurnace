import base64
import binascii
import hmac
import json
import hashlib


class Utils:
    @staticmethod
    def substr(string, start, length=None):
        if start < 0:
            start = start + len(string)
        if not length:
            return string[start:]
        elif length > 0:
            return string[start:start + length]
        else:
            return string[start:length]

    @staticmethod
    def hex2bin(hexdec):
        if hexdec == 'x':
            return False
        if hexdec == '':
            return False
        dec = int(hexdec, 16)
        b = binascii.unhexlify('%x' % dec)
        return b

    @staticmethod
    def base64_url_encode(data):
        return base64.urlsafe_b64encode(data.encode()).replace(b"=", b"").decode()

    @staticmethod
    def base64_url_decode(data):
        return base64.urlsafe_b64decode(data).decode()

    @staticmethod
    def encode_jwt(header, payload, secret):
        body = Utils.base64_url_encode(json.dumps(header)) + "." + Utils.base64_url_encode(json.dumps(payload))
        secret = Utils.hmacsha256(body, secret)
        return body + "." + Utils.base64_url_encode(secret)

    @staticmethod
    def decode_jwt(token: str):
        [headB64, payloadB64, sigB64] = token.split(".")
        rawPayloadJSON = Utils.base64_url_decode(payloadB64)
        if rawPayloadJSON == False:
            raise Exception("Payload base64 is invalid and cannot be decoded")
        decodedPayload = json.loads(rawPayloadJSON)
        if isinstance(decodedPayload, str):
            decodedPayload = json.loads(decodedPayload)
        if not isinstance(decodedPayload, dict):
            raise Exception("Decoded payload should be dict, " + str(type(decodedPayload).__name__) + " received")
        return decodedPayload

    @staticmethod
    def hmacsha256(data, secret):
        encodedData = data.encode()
        byteSecret = secret.encode()
        return hmac.new(byteSecret, encodedData, hashlib.sha256).hexdigest().upper()
