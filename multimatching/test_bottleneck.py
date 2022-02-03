from pdsketch import Diagram

from multimatching import dB


# import pytest

class TestNoMult:
    def test_no_mult(self):
        A = Diagram([(3, 6), (1, 2), (6, 18), (1, 3)])
        B = Diagram([(4, 6), (7, 21)])

        bdist = dB(A, B)
        assert bdist == 3.0
