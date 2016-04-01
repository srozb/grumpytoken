from .CryptoImps import AES256ECB, SHA256
from binascii import a2b_hex, b2a_hex


class BSIDcoder:

    def __init__(self):
        self.key = ""
        self.sid = ""
        self.bsid = ""
        self.pinhash = ""

    def _Unhexify(self, bsidhex):
        bsid = a2b_hex(bsidhex)
        return bsid

    def _Hexify(self, sid):
        sidhex = b2a_hex(sid)
        return sidhex

    def _SetKey(self):
        self.key = self._MakePINHash()

    def _MakePINHash(self, pincode):
        Digest = SHA256.SHA256()
        PINHash = Digest.MultipleHash(pincode, count=2)
        self.pinhash = PINHash
        return PINHash

    def _Decrypt(self):
        Cipher = AES256ECB.AES256ECB(Key=self.key)
        sid = Cipher.Decrypt(self.bsid)
        self.sid = sid

    def _Encrypt(self):
        Cipher = AES256ECB.AES256ECB(Key=self.key)
        bsid = Cipher.Encrypt(self.sid)
        self.bsid = bsid

    def _SetPIN(self, pincode):
        self.pin = pincode.encode('utf-8')
        self._SetKey()

    def GetSID(self):
        if self.sid:
            return self.sid
        else:
            raise Exception("Decode BSID first.")

    def GetSIDHex(self):
        if self.sid:
            return self._Hexify(self.sid)
        else:
            raise Exception("Decode BSID first.")

    def GetBSID(self):
        if self.bsid:
            bsidhex = self.Hexify(self.bsid)
            return bsidhex
        else:
            raise Exception("Enocde SID first.")

    def GetPINHASH(self):
        if self.pinhash:
            return self._Hexify(self.pinhash)
        else:
            raise Exception("No PINHASH set.")

    def Decode(self, bsidhex, pincode):
        self.key = self._MakePINHash(pincode)
        self.bsid = self._Unhexify(bsidhex)
        self._Decrypt()
        return self.GetSID()

    def Encode(self, sid, pincode):
        self.key = self._MakePINHash(pincode)
        self.sid = sid
        self._Encrypt()
        return self.GetBSID()
