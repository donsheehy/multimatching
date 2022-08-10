from graph import Graph
from flow import Flow
import copy
import math

def depth_first_search_with_capacity_priority(residual, s, t, delta):
    S = [(None, s)]
    path = {}
    while S:
        (prev, v) = S.pop()
        if v not in path:
            path[v] = prev
            if v == t:
                break
            for nbr in residual.getNbrs(v):
                if residual[v,nbr] >= delta:
                    S.append((v,nbr))
    return path

def get_s_t_path(path, t):
    if t in path:
        stpath = {}
        current = t
        while path[current] is not None:
            stpath[path[current]] = current
            current = path[current]
        return stpath
    else:
        return False

def augment_s_t_flow(graph, path):
    if path == False:
        return False
    else:
        flow = Flow()
        minCap = float('Inf')
        for e in path:
            currCap = graph[e,path[e]]
            flow.addedge((e, path[e]), 0)
            if currCap < minCap:
                minCap = currCap
        flow.set_all_cap(minCap)
        return flow

def augment_path(residual, s, t, delta):
    return augment_s_t_flow(residual, get_s_t_path(depth_first_search_with_capacity_priority(residual, s, t, delta), t))

def ff_with_capacity_scaling(graph, s, t):
    residual = copy.deepcopy(graph)
    flow = Flow()
    u = graph.get_max_cap()
    delta = 2 ** math.floor(math.log2(u))

    while True:
        path = augment_path(residual, s, t, delta)
        if not path:
            if delta != 1:
                delta /= 2
            else:
                break
        else:
            flow += path
            residual -= path
            path = augment_path(residual, s, t, delta)

    maxFlow = 0
    for nbr in flow.getNbrs(s):
        maxFlow += flow[s,nbr]

    return maxFlow
