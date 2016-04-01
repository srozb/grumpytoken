from Crypto.Cipher import AES


class AES256ECB:

    def __init__(self, Key):
        self.Key = Key

    def Encrypt(self, Plaintext):
        cipher = AES.new(self.Key, AES.MODE_ECB)
        Ciphertext = cipher.encrypt(Plaintext)
        return Ciphertext

    def Decrypt(self, Ciphertext):
        cipher = AES.new(self.Key, AES.MODE_ECB)
        Plaintext = cipher.decrypt(Ciphertext)
        return Plaintext