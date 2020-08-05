from BJUTLabServer.utilities.Crypto import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

with open('test_rsa_key', 'rb') as f:
    rsa_key = f.read()

Crypto.load_config({
    'aes': b'12345678123456781234567812345678',
    'rsa': rsa_key,
    'nonce': b'12345678'
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
    HeiseiDebtKing = '世界中が君を信じてる、二つのパワーで、戦え！ウルトラマンオーブ！'.encode()  # ?
    key = RSA.import_key(rsa_key)
    pub_key = key.publickey()
    cipher_array = []
    cipher = PKCS1_OAEP.new(pub_key)
    for i in range(0, len(HeiseiDebtKing), 200):
        cipher_array.append(cipher.encrypt(HeiseiDebtKing[i:i + 200]))
    cipher_bytes = b''.join(cipher_array)
    assert Crypto.Decrypt.rsa(cipher_bytes) == HeiseiDebtKing
    # 由于pycryptodome不能用公钥解密（虽然是用私钥加密的），所以没法测试Crypto.Encrypt.rsa()
