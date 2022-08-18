from graph import Graph
from flow import Flow
import ford_fulkerson
import capacity_scaling
import dinics
import unittest

class Test_Graph(unittest.TestCase):
    def testGraph(self):
        G = Graph([1,2,3,4,5,6,7], {(1,2,1), (1,3,2), (2,4,3), (2,5,2), (3,6,3), (5,7,4)})
        self.assertEqual(G[1,2], 1)

    def testFF(self):
        G = Graph([1,2,3,4,5,6,7], {(1,2,1), (1,3,2), (2,4,3), (2,5,2), (3,6,3), (5,7,4)})
        self.assertEqual(ford_fulkerson.fordfulkerson(G, 1, 7), 1)

        G = Graph([1,2,3,4,5,6], {(1,2,11), (1,3,12), (2,4,12), (3,2,1), (3,5,11), (5,4,7), (5,6,4), (4,6,19)})
        self.assertEqual(ford_fulkerson.fordfulkerson(G, 1, 6), 23)

        G = Graph([0,1,2,3,4,5], {(0,1,10), (0,2,10), (1,2,2), (1,3,4), (1,4,8), (2,4,9), (4,3,6), (3,5,10), (4,5,10)})
        self.assertEqual(ford_fulkerson.fordfulkerson(G, 0, 5), 19)

        G = Graph([1,2,3,4], {(1,2,1000), (1,3,1000), (2,3,1), (2,4,1000), (3,4,1000)})
        self.assertEqual(ford_fulkerson.fordfulkerson(G, 1, 4), 2000)

    def testCapScaling(self):
        G = Graph([1,2,3,4,5,6,7], {(1,2,1), (1,3,2), (2,4,3), (2,5,2), (3,6,3), (5,7,4)})
        self.assertEqual(capacity_scaling.ff_with_capacity_scaling(G, 1, 7), 1)

        G = Graph([1,2,3,4,5,6], {(1,2,11), (1,3,12), (2,4,12), (3,2,1), (3,5,11), (5,4,7), (5,6,4), (4,6,19)})
        self.assertEqual(capacity_scaling.ff_with_capacity_scaling(G, 1, 6), 23)

        G = Graph([0,1,2,3,4,5], {(0,1,10), (0,2,10), (1,2,2), (1,3,4), (1,4,8), (2,4,9), (4,3,6), (3,5,10), (4,5,10)})
        self.assertEqual(capacity_scaling.ff_with_capacity_scaling(G, 0, 5), 19)

        G = Graph([1,2,3,4], {(1,2,1000), (1,3,1000), (2,3,1), (2,4,1000), (3,4,1000)})
        self.assertEqual(capacity_scaling.ff_with_capacity_scaling(G, 1, 4), 2000)

    def testDinics(self):
        G = Graph([0,1,2,3,4,5], {(0,1,10), (0,2,10), (1,2,2), (1,3,4), (1,4,8), (2,4,9), (4,3,6), (3,5,10), (4,5,10)})
        self.assertEqual(dinics.dinics(G, 0, 5), 19)

        G = Graph([1,2,3,4,5,6], {(1,2,11), (1,3,12), (2,4,12), (3,2,1), (3,5,11), (5,4,7), (5,6,4), (4,6,19)})
        self.assertEqual(dinics.dinics(G, 1, 6), 23)

        G = Graph([1,2,3,4,5,6,7], {(1,2,1), (1,3,2), (2,4,3), (2,5,2), (3,6,3), (5,7,4)})
        self.assertEqual(dinics.dinics(G, 1, 7), 1)

        G = Graph([1,2,3,4], {(1,2,1000), (1,3,1000), (2,3,1), (2,4,1000), (3,4,1000)})
        self.assertEqual(dinics.dinics(G, 1, 4), 2000)

if __name__ == "__main__":
    unittest.main()