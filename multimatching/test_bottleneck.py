from pdsketch import Diagram
import unittest
from multimatching import dB

class TestDBwithMult(unittest.TestCase):
    def test_no_mult(self):
        A = Diagram([(3, 6), (1, 2), (6, 18), (1, 3)])
        B = Diagram([(4, 6), (7, 21)])
        self.assertEqual(dB(A, B), 3.0)

    def test_one_point_with_mult(self):
        #  Two diagrams with multiplicity
        A = Diagram([(0,6)],[1000000000])
        B = Diagram([(1,6)],[1000000000])
        self.assertEqual(dB(A,B), 1.0)

    def test_one_point_with_different_mults(self):
        #  Two diagrams with multiplicity
        A = Diagram([(0,6)],[1000000001])
        B = Diagram([(1,6)],[1000000000])
        self.assertEqual(dB(A,B), 3.0)

    def test_multiple_points_with_different_mults(self):
        #  Two diagrams with multiplicity with points close to the diagonal
        A = Diagram([(0,6), (0,1)],[1000000001, 100])
        B = Diagram([(100, 101), (1,6)],[50, 1000000000])
        self.assertEqual(dB(A,B), 3.0)

    def test_unequal_size_base_sets(self):
        #  Two diagrams with different numbers of distinct points.
        A = Diagram([(0,6), (0,1)],[1000000001, 100])
        B = Diagram([(1,6), (100, 101), (0,8)],[1000000000, 50, 1])
        self.assertEqual(dB(A,B), 2.0)




if __name__ == '__main__':
    unittest.main()
