import hashlib


class Encryptor:

    @staticmethod
    def md5(content):
        return hashlib.md5(content.encode(encoding='utf8')).hexdigest()
