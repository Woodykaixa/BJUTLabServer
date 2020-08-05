"""
`Crypto.py` 提供了MD5、AES、RSA加密和解密算法，封装自`pycryptodome`。
"""
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES, PKCS1_OAEP


class Crypto:
    """
    提供加密和解密。
    """
    _KEYS = None

    @staticmethod
    def load_config(secret_keys: dict):
        """
        设置密钥字典。
        :param secret_keys: 密钥字典
        """
        Crypto._KEYS = secret_keys

    class Encrypt:

        @staticmethod
        def md5(content: str):
            """
            MD5加密。
            :param content: 待加密字符串
            :return: 加密后的字符串
            """
            return MD5.new(content.encode('utf8')).hexdigest()

        @staticmethod
        def aes(content: str):
            """
            AES加密
            :param content: 待加密字符串
            :return: 密文的字节数组
            """
            cipher = AES.new(Crypto._KEYS['aes'], AES.MODE_GCM, nonce=Crypto._KEYS['nonce'])
            return cipher.encrypt(pad(content.encode('utf8'), AES.block_size))

        @staticmethod
        def rsa(content: str):
            """
            RSA加密。
            :param content: 待加密字符串
            :return: 密文的字节数组
            """
            content_byte = content.encode()
            BLOCK_SIZE = 200
            result = []
            key = RSA.import_key(Crypto._KEYS['rsa'])
            cipher = PKCS1_OAEP.new(key)
            for i in range(0, len(content_byte), BLOCK_SIZE):
                result.append(cipher.encrypt(content_byte[i:i + BLOCK_SIZE]))
            return b''.join(result)

    class Decrypt:

        @staticmethod
        def aes(cipher_bytes: bytes):
            """
            AES解密。
            :param cipher_bytes: 密文
            :return: 解密出的明文
            """
            cipher = AES.new(Crypto._KEYS['aes'], AES.MODE_GCM, nonce=Crypto._KEYS['nonce'])
            return unpad(cipher.decrypt(cipher_bytes), AES.block_size).decode()

        @staticmethod
        def rsa(cipher_bytes: bytes):
            """
            RSA解密。
            :param cipher_bytes: 密文
            :return: 解密出的明文
            """
            BLOCK_SIZE = 256
            result = []
            key = RSA.import_key(Crypto._KEYS['rsa'])
            cipher = PKCS1_OAEP.new(key)
            for i in range(0, len(cipher_bytes), BLOCK_SIZE):
                result.append(cipher.decrypt(cipher_bytes[i:i + BLOCK_SIZE]))
            return b''.join(result)
