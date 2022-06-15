from edge_function_class import EdgeFunction
import math

class Graph:    
    #initializes graph
    def __init__(self, V, E):
        self.capacity = EdgeFunction()
        self._nbrs = {}
        for u,v,c in E:
            self.addedge(u,v,c)
        for v in V:
            self.addvertex(v)
    
    #adds vertex
    def addvertex(self, v):
        if v not in self._nbrs:
            self._nbrs[v] = set()

    #adds edge
    def addedge(self, u, v, c):
        self.addvertex(u)
        self.addvertex(v)
        self.capacity[u,v] = c
        self._nbrs[u].add(v)
        self._nbrs[v].add(u)

    #removes edge
    def removeedge(self, u, v):
        del self.capacity[u,v]
        self._nbrs[u].remove(v)
        self._nbrs[v].remove(u)

    #removes vertex
    def removevertex(self, u):
        todelete = list(self.nbrs(u))
        for v in todelete:
            self.removeedge(u,v)
        del self._nbrs[u]

    #returns degree of vertex
    def deg(self, v):
        return len(self._nbrs[v])

    #return the capacity of a certain edge
    def capEdge(self, u, v):
        return self.capacity[u,v]

    #returns neighbors of a vertex as an iterator
    def nbrs(self, v):
        return iter(self._nbrs[v])

    #returns number of edges
    @property
    def m(self):
        return len(self.cap)

    #returns number of vertices
    @property
    def n(self):
        return len(self._nbrs)

    #return the edge function obj of capacities
    @property
    def cap(self):
        return self.capacity

    #depth first search, returns path of search
    def dfs(self, residual, s, t):
        S = [(None, s)] #stack used during search
        path = {} #dict that stores path of travel of search
        while S:
            (prev,v) = S.pop()
            if v not in path:
                path[v] = prev
                if v == t:
                    break
                for nbr in self.nbrs(v):
                    if residual[(v, nbr)] > 0:
                        S.append((v,nbr))
        return path

    #get the path to the root from dict of path
    def stpath(self, t, path):
        if t in path:
            pathToS = {} #dict to store the final path of the flow from start of path to t
            current = t
            while path[current] is not None:
                pathToS[path[current]] = current
                current = path[current]
            return pathToS
        else:
            return False

    #returns a flow of minimum capacity on the path
    def augmentFlow(self, residual, path):
        if path == False:
            return False
        else: 
            pathFlow = EdgeFunction() #path flow
            for a in path:
                pathFlow[(a,path[a])] = residual[(a,path[a])]
            pathFlow.set_all_cap(pathFlow.min_cap())
            return pathFlow

    #does the steps above in one function for easy reading
    def augmentPath(self, residual, s, t):
        return self.augmentFlow(residual, self.stpath(t, self.dfs(residual, s, t)))

    #implementation of ford fulkerson algorithm
    def fordfulkerson(self, s, t):
        residualG = EdgeFunction()
        flow = EdgeFunction()
        residualG += self.cap
        path = self.augmentPath(residualG, s, t)
        while path:
            flow += path
            flow.reverseSub(path)
            residualG -= path
            path = self.augmentPath(residualG, s, t)
        
        maxFlow = 0
        for nbr in self.nbrs(s):
            maxFlow += flow[(s,nbr)]

        return maxFlow

    #depth first search with a capacity bound
    def dfsWithCapPriority(self, residual, s, t, delta):
        S = [(None, s)] #stack used during search
        path = {} #dict that stores path of travel of search
        while S:
            (prev,v) = S.pop()
            if v not in path:
                path[v] = prev
                if v == t:
                    break
                for nbr in self.nbrs(v):
                    if residual[(v, nbr)] >= delta:
                        S.append((v,nbr))
        return path

    #augmenting path method from earlier except uses the dfs with cap bound instead of normal dfs
    def augmentPathWithCapPriority(self, residual, s, t, delta):
        return self.augmentFlow(residual, self.stpath(t, self.dfsWithCapPriority(residual, s, t, delta)))

    #implementation of ford fulkerson that uses capacity scaling for better path finding
    def capacity_scaling_alg(self, s, t):
        residualG = EdgeFunction()
        flow = EdgeFunction()
        residualG += self.cap
        u = residualG.max_cap()
        delta = int(2 ** (len(format(u, "b")))) / 2 if math.log2(u) % 1 == 0 else int(2 ** (len(format(u, "b"))))

        while True:
            path = self.augmentPathWithCapPriority(residualG, s, t, delta)
            if not path:
                if delta != 1:
                    delta /= 2
                else:
                    break
            else: 
                flow += path
                flow.reverseSub(path)
                residualG -= path

        maxFlow = 0
        for nbr in self.nbrs(s):
            maxFlow += flow[(s,nbr)]

        return maxFlow