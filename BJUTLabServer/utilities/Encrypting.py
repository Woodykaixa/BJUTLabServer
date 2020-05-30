"""
`Encrypting.py` 提供了一个 :class:`Encryptor` 用于加密字符串。
"""
import hashlib


class Encryptor:
    """
    提供加密方法，目前仅封装了MD5。
    """
    @staticmethod
    def md5(content: str):
        """
        调用 `hashlib` 提供的md5方法进行加密。
        :param content: 待加密字符串
        :return: 加密后的字符串
        """
        return hashlib.md5(content.encode(encoding='utf8')).hexdigest()
