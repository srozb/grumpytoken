from .Converter import Converter
from .CryptoImps import SHA256
from struct import pack
from binascii import a2b_hex, b2a_hex
from time import localtime


class Token:

    def __init__(self, SIDHex):
        self.TokenNum = ""
        self.TokenValue = ""
        self.SID = ""
        self.SIDHex = SIDHex
        self.PointInTime = 0
        self.VendorTimeOffset = 3600  # GMT + 1 - Warsaw
        self.TimeTolerance = 60
        self.SetSIDHex(SIDHex)

    def _GetVendorTimeOffset(self):
        #Hardcoded timezone for Warsaw + optional daylight savings time.
        VendorTimeOffset = self.VendorTimeOffset + 3600 * localtime().tm_isdst
        return VendorTimeOffset

    def _MakeTimeStr(self):
        T = int(self.PointInTime)
        B = pack('BBBB', int(0xFF & T), int(0xFF & T >> 8),
        int(0xFF & T >> 16), int(0xFF & T >> 24))
        TimeStr = B
        return TimeStr

    def _PopulateTokenValue(self, Token):
        self.TokenValue = Token
        self.TokenNum = Converter().bin2num(Token)

    def SetSID(self, sid):
        self.SID = sid

    def SetSIDHex(self, sidhex):
        self.SID = a2b_hex(sidhex)

    def _ConvertEpoch(self, epoch):
        VendorTimeOffset = self._GetVendorTimeOffset()
        VendorTime = round((epoch + VendorTimeOffset) / self.TimeTolerance)
        self.PointInTime = VendorTime

    def GetPointInTime(self):
        return self.PointInTime

    def GetTokenNum(self):
        return self.TokenNum

    def GetTokenValue(self):
        return b2a_hex(self.TokenValue)

    def Generate(self, TargetEpoch):
        Digest = SHA256.SHA256()
        self._ConvertEpoch(TargetEpoch)
        TimeStr = self._MakeTimeStr()
        Seed = (self.SID, TimeStr, self.SID)
        Token = Digest.ConcatHash(Seed)
        #print(b2a_hex(Token))
        self._PopulateTokenValue(Token)
        return self.TokenNum
