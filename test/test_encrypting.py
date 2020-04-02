import util.Encrypting as E


def test_md5():
    assert len(E.Encryptor.md5('LABxhjj1802@#')) == 32
