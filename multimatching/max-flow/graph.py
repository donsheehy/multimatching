class Graph:
    def __init__(self, V = None, E = None):
        self._edges = []
        self.values = {}
        if E is not None:
            for u,v,c in E:
                self.addedge((u,v),c)
        if V is not None:
            for v in V:
                self.addvertex(v)

    def __getitem__(self,E):
        (u,v) = E
        key = self.values.get(u, None)
        if key is not None:
            return self.values.get(u, None).get(v, 0)
        else:
            return 0

    def __setitem__(self,E,value):
        (u,v) = E
        try:
            self.values[u][v] = value
        except KeyError:
            self.values[u] = {v: value}

    def __delitem__(self,E):
        (u,v) = E
        del self.values[u][v]

    def addvertex(self,v):
        if v not in self.values:
            self.values[v] = {}

    def addedge(self,E,c):
        (u,v) = E
        self.addvertex(u)
        self.addvertex(v)
        self[u,v] = c
        self[v,u] = 0
        self._edges.append(E)

    def removevertex(self,v):
        for nbr in self[v]:
            del self[nbr,v]
        del self[v]

    def removeedge(self,E):
        (u,v) = E
        del self[u,v]
        del self[v,u]
        self._edges.remove(E)

    def getNbrs(self, k):
        return self.values[k].keys()

    def get_values(self):
        return self.values

    def get_min_cap(self):
        min = float('Inf')
        for u,v in self._edges:
            if self[u,v] < min and self[u,v] > 0:
                min = self[u,v]
        return min

    def get_max_cap(self):
        max = 0
        for u,v in self._edges:
            if self[u,v] > max:
                max = self[u,v]
        return max

    def __iadd__(self, other):
        for u in other.get_values().keys():
            vals = other.values[u]
            for v in vals.keys():
                self[u,v] += other[u,v]
        return self

    def __isub__(self, other):
        for u in other.get_values().keys():
            vals = other.values[u]
            for v in vals.keys():
                self[u,v] -= other[u,v]
        return self

    def __iter__(self):
        return iter(self.values)

    def __str__(self):
        return str(self.values)

    def set_all_cap(self, c):
        for u,v in self._edges:
            self[u,v] = c
