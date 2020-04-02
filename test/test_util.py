import os


def test_plus_tuple():
    t1 = (1, 2)
    t2 = ('3', [4, 5])
    t3 = t1 + t2
    assert t3 == (1, 2, '3', [4, 5])

