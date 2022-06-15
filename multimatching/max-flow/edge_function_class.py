from collections import defaultdict

class EdgeFunction(defaultdict):
    #initialize the edge
    def __init__(self):
        super(EdgeFunction, self).__init__(lambda:0)

    #incrementally adds every value in edge with value of passed object
    def __iadd__(self, other):
        for k in other.keys():
            self[k] += other[k]
        return self

    #incrementally subtracts every value in edge with value of passed object
    def __isub__(self, other):
        for k in other.keys():
            self[k] -= other[k]
        return self

    #defines creating an iterator
    def __iter__(self):
        return iter(self.values)

    #returns the minimum capacity of an edge in the list
    def min_cap(self):
        return min(self.values())

    #returns max capacity in the edge function
    def max_cap(self):
        return max(self.values())

    #sets all capacities to the same integer
    def set_all_cap(self, i):
        for e in self.keys():
            self[e] = i

    #subtracts other from the reverse of the edge (vu instead of uv)
    def reverseSub(self, other):
        for k in other.keys():
            x,y = k[0], k[1]
            self[y, x] -= other[x, y]