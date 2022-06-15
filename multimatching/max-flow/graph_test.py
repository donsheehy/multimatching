from graph_class import Graph
from edge_function_class import EdgeFunction
import unittest

class Test_Graph(unittest.TestCase):

    def testDFS(self):
        G = Graph([1,2,3,4,5,6,7], {(1,2,1), (1,3,2), (2,4,3), (2,5,2), (3,6,3), (5,7,4)})
        print(G.stpath(7, G.dfs(G.cap, 1, 7)))
        print(G.dfs(G.cap, 1,7))

        G = Graph(["s", "x1", "x2", "x3", "y1", "y2", "y3", "t"], 
            {("s","x1",1),("s","x2",1),("s","x3",1),("x1","y1",1),("x1","y2",1),("x2","y2",1),("x2","y3",1),("x3","y3",1),("y1","t",1),("y2","t",1),("y3","t",1)})
        print(G.dfs(G.cap, "s", "t"))

    def testEdgeFunction(self):
        E = EdgeFunction()
        E[(1,2)] = 10
        E[(1,3)] = 20
        E[(2,4)] = 30
        E[(2,5)] = 15
        E[(4,5)] = 16

        del E[(2,5)]
        self.assertEqual(E[(1,2)], 10)
        self.assertEqual(E[(1,3)], 20)
        self.assertEqual(E[(2,4)], 30)
        self.assertEqual(E[(4,5)], 16)
        self.assertEqual(E.min_cap(), 10)

        F = EdgeFunction()
        F[(1,2)] = 5
        F[(1,3)] = 10
        F[(2,4)] = 2
        F[(2,5)] = 4
        F[(4,5)] = 7

        E += F
        self.assertEqual(E[(1,2)], 15)
        self.assertEqual(E[(1,3)], 30)
        self.assertEqual(E[(2,4)], 32)
        self.assertEqual(E[(2,5)], 4)
        self.assertEqual(E[(4,5)], 23)

        E -= F
        self.assertEqual(E[(1,2)], 10)
        self.assertEqual(E[(1,3)], 20)
        self.assertEqual(E[(2,4)], 30)
        self.assertEqual(E[(2,5)], 0)
        self.assertEqual(E[(4,5)], 16)

        E.set_all_cap(2)
        self.assertEqual(E[(1,2)], 2)
        self.assertEqual(E[(1,3)], 2)
        self.assertEqual(E[(2,4)], 2)
        self.assertEqual(E[(2,5)], 2)
        self.assertEqual(E[(4,5)], 2)

    def testFordFulkerson(self):
        G = Graph([1,2,3,4], {(1,2,1000), (1,3,1000), (2,3,1), (2,4,1000), (3,4,1000)})
        self.assertEqual(G.fordfulkerson(1,4), 2000)

        G = Graph([1,2,3,4,5,6,7], {(1,2,1), (1,3,2), (2,4,3), (2,5,2), (3,6,3), (5,7,4)})
        self.assertEqual(G.fordfulkerson(1,7), 1)

        G = Graph([1,2,3,4,5,6], {(1,2,11), (1,3,12), (2,4,12), (3,2,1), (3,5,11), (5,4,7), (5,6,4), (4,6,19)})
        self.assertEqual(G.fordfulkerson(1,6), 23)

        #this one is not solving right
        G = Graph([0,1,2,3,4,5], {(0,1,10), (0,2,10), (1,2,2), (1,3,4), (1,4,8), (2,4,9), (4,3,6), (3,5,10), (4,5,10)})
        self.assertEqual(G.fordfulkerson(0,5), 19)

    def testCapScalingAlg(self):
        G = Graph([1,2,3,4], {(1,2,1000), (1,3,1000), (2,3,1), (2,4,1000), (3,4,1000)})
        self.assertEqual(G.capacity_scaling_alg(1,4), 2000)

        G = Graph([1,2,3,4,5,6,7], {(1,2,1), (1,3,2), (2,4,3), (2,5,2), (3,6,3), (5,7,4)})
        self.assertEqual(G.capacity_scaling_alg(1,7), 1)

        G = Graph([1,2,3,4,5,6], {(1,2,11), (1,3,12), (2,4,12), (3,2,1), (3,5,11), (5,4,7), (5,6,4), (4,6,19)})
        self.assertEqual(G.capacity_scaling_alg(1,6), 23)

        G = Graph([0,1,2,3,4,5], {(0,1,10), (0,2,10), (1,2,2), (1,3,4), (1,4,8), (2,4,9), (4,3,6), (3,5,10), (4,5,10)})
        self.assertEqual(G.capacity_scaling_alg(0,5), 19)

if __name__ == "__main__":
    unittest.main()