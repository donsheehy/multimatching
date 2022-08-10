from graph import Graph

class Flow(Graph):
    def __init__(self, V = None, E = None):
        super().__init__(V, E)

    def __setitem__(self, E, value):
        (u,v) = E
        try:
            self.values[u][v] = value
        except KeyError:
            self.values[u] = {v: value}
        try:
            self.values[v][u] = -1 * value
        except KeyError:
            self.values[v] = {u: -1 * value}

    def addedge(self, E, c):
        (u,v) = E
        self.addvertex(u)
        self.addvertex(v)
        self[u,v] = c

    def __iadd__(self, other):
        for u in other.get_values().keys():
            vals = other.values[u]
            for v in vals.keys():
                super().__setitem__((u,v), self[u,v] + other[u,v])
        return self

    def __isub__(self, other):
        for u in other.get_values().keys():
            vals = other.values[u]
            for v in vals.keys():
                super().__setitem__((u,v), self[u,v] - other[u,v])
        return self

    def set_all_cap(self, c):
        for u in self.get_values().keys():
            vals = self.values[u]
            for v in vals.keys():
                self[u,v] = c
                self[v,u] = -c