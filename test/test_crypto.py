from BJUTLabServer.utilities.Crypto import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

with open('test_rsa_key', 'rb') as f:
    rsa_key = f.read()

Crypto.load_config({
    'AES_KEY': b'12345678123456781234567812345678',
    'RSA_PRI_KEY': rsa_key
})


def test_aes():
    lemon = 'あの日の悲しみさえ、あの日の苦しみさえ、そのすべてを愛してたあなたとともに'  # ?
    cipher = Crypto.Encrypt.aes(lemon)
    result = Crypto.Decrypt.aes(cipher)
    assert result == lemon


def test_md5():
    result = Crypto.Encrypt.md5('世界中が君を待っている、闇夜を照らせ光の戦士よ')  # ?
    assert result == '89708c3016ed29e4698e7bed0be969bc'


def test_rsa():
    HeiseiDebtKing = '戦え！ウルトラマンオーブ！'.encode()  # ?
    key = RSA.import_key(rsa_key)
    pub_key = key.publickey()
    pub_cipher = PKCS1_OAEP.new(pub_key)
    cipher_bytes = pub_cipher.encrypt(HeiseiDebtKing)
    assert Crypto.Decrypt.rsa(cipher_bytes) == HeiseiDebtKing
