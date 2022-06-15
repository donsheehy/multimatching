class EdgeFunction:
    #initialize the edge
    def __init__(self):
        self.values = {}
    
    #returns item at index
    def __getitem__(self, index):
        return self.values.get(index, 0)

    #sets item at key to the value
    def __setitem__(self, key, value):
        self.values[key] = value

    #deletes item with key
    def __delitem__(self, key):
        del self.values[key]

    #incrementally adds every value in edge with value of passed object
    def __iadd__(self, other):
        for k,v in other.items():
            try:
                self.values[k] += v
            except:
                self.values[k] = v
        return self

    #incrementally subtracts every value in edge with value of passed object
    def __isub__(self, other):
        for k,v in other.items():
            try:
                self.values[k] -= v
            except:
                self.values[k] = -v
        return self

    #defines creating an iterator
    def __iter__(self):
        return iter(self.values)

    #returns the items in the list
    def items(self):
        return self.values.items()

    #returns the minimum capacity of an edge in the list
    def min_cap(self):
        return self.values[min(self.values, key = self.values.get)]

    #sets all capacities to the same integer
    def set_all_cap(self, i):
        for key in self.values:
            self.values[key] = i

    #returns length of list
    def __len__(self):
        return len(self.values)

    #subtracts other from the reverse of the edge (vu instead of uv)
    def reverseSub(self, other):
        for k,v in other.items():
            x,y = k[0], k[1]
            try:
                self.values[y, x] -= v
            except:
                self.values[y, x] = -v
            
    #returns max capacity in the edge function
    def max_cap(self):
        return(max(self.values.values()))