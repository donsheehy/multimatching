import unittest

from pdsketch import Diagram, PDPoint
from multimatching import dB


class TestDBwithMult(unittest.TestCase):
    def test_no_mult(self):
        diagonal_pd_point = PDPoint((0.0, 0.0))
        A = Diagram([(3, 6), (1, 2), (6, 18), (1, 3)])
        B = Diagram([(4, 6), (7, 21)])
        expected_matching = {diagonal_pd_point: {diagonal_pd_point: 1, PDPoint((4.0, 6.0)): 1},
                             PDPoint((1.0, 2.0)): {diagonal_pd_point: 1},
                             PDPoint((1.0, 3.0)): {diagonal_pd_point: 1},
                             PDPoint((3.0, 6.0)): {diagonal_pd_point: 1},
                             PDPoint((6.0, 18.0)): {PDPoint((7.0, 21.0)): 1}}

        bottleneck_distance, matching = dB(A, B, get_matching=True)

        self.assertEqual(matching, expected_matching)
        self.assertEqual(bottleneck_distance, 3.0)

    def test_one_point_with_mult(self):
        #  Two diagrams with multiplicity
        diagonal_pd_point = PDPoint((0.0, 0.0))
        point_a = PDPoint((0.0, 6.0))
        point_b = PDPoint((1.0, 6.0))
        multiplicity_one_billion = 1000000000
        A = Diagram([point_a], [multiplicity_one_billion])
        B = Diagram([point_b], [multiplicity_one_billion])
        expected_matching = {diagonal_pd_point: {diagonal_pd_point: multiplicity_one_billion},
                             point_a: {point_b: multiplicity_one_billion}}

        bottleneck_distance, matching = dB(A, B, get_matching=True)

        self.assertEqual(matching, expected_matching)
        self.assertEqual(bottleneck_distance, 1.0)

    def test_one_point_with_different_mults(self):
        #  Two diagrams with unequal multiplicity
        A = Diagram([(0, 6)], [1000000000])
        B = Diagram([(1, 6)], [1000000001])
        bottleneck_distance, matching = dB(A, B, get_matching=True)
        self.assertEqual(bottleneck_distance, 2.5)

    def test_multiple_points_with_different_mults(self):
        diagonal_pd_point = PDPoint((0.0, 0.0))
        #  Two diagrams with multiplicity with points close to the diagonal
        A = Diagram([(0, 6), (0, 1)], [1000000001, 100])
        B = Diagram([(100, 101), (1, 6)], [50, 1000000000])

        bottleneck_distance, matching = dB(A, B, get_matching=True)

        expected_matching = {PDPoint((0.0, 1.0)): {diagonal_pd_point: 100},
                             PDPoint((0.0, 0.0)): {PDPoint((100.0, 101.0)): 50,
                                                   PDPoint((1.0, 6.0)): 1000000000},
                             PDPoint((0.0, 6.0)): {diagonal_pd_point: 1000000001}}
        expected_matching = expected_matching
        self.assertEqual(matching, expected_matching)
        self.assertEqual(bottleneck_distance, 3.0)

    def test_unequal_size_base_sets(self):
        #  Two diagrams with different numbers of distinct points.
        A = Diagram([(0, 6), (0, 1)], [1000000001, 100])
        B = Diagram([(1, 6), (100, 101), (0, 8)], [1000000000, 50, 1])

        bottleneck_distance, matching = dB(A, B, get_matching=True)
        self.assertEqual(bottleneck_distance, 2.0)

    def test_infinite_coords_with_no_mult(self):
        diagonal_pd_point = PDPoint((0.0, 0.0))
        point_a = PDPoint((0.0, float('inf')))
        point_b = PDPoint((2.0, float('inf')))
        A = Diagram([point_a])
        B = Diagram([point_b])

        bottleneck_distance, matching = dB(A, B, get_matching=True)
        expected_matching = {diagonal_pd_point: {diagonal_pd_point: 1},
                             point_a: {point_b: 1}}
        self.assertEqual(matching, expected_matching)
        self.assertEqual(bottleneck_distance, 2.0)

    def test_infinite_coords_with_equal_mult(self):
        diagonal_pd_point = PDPoint((0.0, 0.0))
        point_a = PDPoint((0.0, float('inf')))
        point_b = PDPoint((2.0, float('inf')))
        A = Diagram([point_a], [500])
        B = Diagram([point_b], [500])
        bottleneck_distance, matching = dB(A, B, get_matching=True)
        expected_matching = {diagonal_pd_point: {diagonal_pd_point: 500},
                             point_a: {point_b: 500}}
        self.assertEqual(matching, expected_matching)
        self.assertEqual(bottleneck_distance, 2.0)

    def test_infinite_coords_with_unequal_mult(self):
        A = Diagram([(0, float('inf'))], [501])
        B = Diagram([(2, float('inf'))], [500])
        bottleneck_distance, matching = dB(A, B, get_matching=True)
        self.assertEqual(bottleneck_distance, float('inf'))

    def test_finite_and_infinite_points_with_mult(self):
        A = Diagram([(0, float('inf')), (0, 6)], [500, 2])
        B = Diagram([(2, float('inf')), (0, 7)], [500, 2])
        bottleneck_distance, matching = dB(A, B, get_matching=True)
        self.assertEqual(bottleneck_distance, 2.0)

    def test_distance_with_self(self):
        point_a = PDPoint((6.0, 12345.0))
        diagonal_pd_point = PDPoint((0.0, 0.0))
        A = Diagram([point_a], [15])
        bottleneck_distance, matching = dB(A, A, get_matching=True)
        expected_matching = {point_a: {point_a: 15},
                             diagonal_pd_point: {diagonal_pd_point: 15}}
        self.assertEqual(matching, expected_matching)
        self.assertEqual(bottleneck_distance, 0)

    def test_mult_without_mass_list(self):
        diagonal_pd_point = PDPoint((0.0, 0.0))
        point_a = PDPoint((0.0, 6.0))
        point_b = PDPoint((1.0, 6.0))
        A = Diagram([point_a], [1])
        B = Diagram([point_b])
        bottleneck_distance, matching = dB(A, B, get_matching=True)
        expected_matching = {diagonal_pd_point: {diagonal_pd_point: 1},
                             point_a: {point_b: 1}}
        self.assertEqual(matching, expected_matching)
        self.assertEqual(bottleneck_distance, 1.0)

    def test_matching_on_three_points(self):
        A = Diagram([(2, 3), (5, 10)], [3, 4])
        B = Diagram([(5, 11), (9, 10)], [1, 6])
        bottleneck_distance, matching = dB(A, B, get_matching=True)
        self.assertEqual(bottleneck_distance, 2.5)


if __name__ == '__main__':
    unittest.main()
