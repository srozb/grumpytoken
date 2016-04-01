from hashlib import sha256


class SHA256:

    def __init__(self):
        ""

    def Hash(self, data):
        Hash = sha256()
        try:
            Hash.update(data.encode('utf-8'))
        except:
            Hash.update(data)
        return Hash.digest()

    def MultipleHash(self, data, count):
        for i in range(count):
            data = self.Hash(data)
        return data

    def ConcatHash(self, datatable):
        Hash = sha256()
        for data in datatable:
            Hash.update(data)
        return Hash.digest()
