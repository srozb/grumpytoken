#from binascii import b2a_hex
from struct import unpack


class Converter:

    def __init__(self):
        ""

    def Padding(self, buf, length=8, padbyte=b'\x00'):
        "Structure unpack needs exact length."
        return (length - len(buf)) * padbyte

    def bin2num(self, binary, strlen=8):
        NumericalToken = ""
        ExtractionPoints = [(0, 7), (7, 13)]  # Wheel uses 2 out of 4 by def.
        for EP in ExtractionPoints:
            "Extract interesting bytes from SHA256 digest"
            subbinary = binary[EP[0]:EP[1]]
            padding = self.Padding(subbinary)
            buf = padding + subbinary
            subbinary_value = str(unpack('>Q', buf)[0])
            NumericalToken += subbinary_value[-4:]
        return NumericalToken[:strlen]
