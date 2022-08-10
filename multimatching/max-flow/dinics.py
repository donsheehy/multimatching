from operator import ne
from graph import Graph
from flow import Flow
import copy
import math

def generate_level_graph(graph, s, t):
    Q = [s]
    levelgraph = Graph()
    tFound = False
    while Q:
        v = Q.pop(0)
        if v == t:
            tFound = True
            continue
        for nbr in graph.getNbrs(v):
            if ((nbr not in levelgraph and not tFound) or nbr == t) and graph[v,nbr] > 0:
                levelgraph.addedge((v, nbr), graph[v, nbr])
                Q.append(nbr)
    return levelgraph

def depth_first_search_with_levels(levelgraph, s, t):
    S = [(None, s)]
    visited = []
    path = []
    while S:
        (prev, v) = S.pop()
        if v not in visited or v == t:
            visited.append(v)
            path.append((prev, v))
            if v == t:
                continue
            for nbr in levelgraph.getNbrs(v):
                if levelgraph[v,nbr] > 0:
                    S.append((v,nbr))
    return path

def generate_blocking_flow(levelgraph, path, t):
    blockingFlow = Flow()
    currentPath = Flow()
    prev = path.pop(0)
    backtrack = [prev]
    while path:
        (u,v) = path.pop(0)
        currentPath.addedge((u,v), levelgraph[u,v])
        if v == t:
            currentPath.set_all_cap(currentPath.get_min_cap())
            blockingFlow += currentPath
            currentPath = Flow()
            del backtrack[1:]
            if len(path) != 0:
                prev = path.pop(0)
                backtrack.append(prev)
                (u,v) = prev
                currentPath.addedge((u,v), levelgraph[u,v])
        elif prev[1] != u:
            (a,b) = prev
            currentPath.removeedge(a,b)
            if len(path) == 0:
                continue
            (c,d) = path[0]
            (a,b) = backtrack.pop()
            (a,b) = backtrack.pop()
            prev = (a,b)
            while not (b == u and v == c):
                currentPath.removeedge(a,b)
                if len(backtrack) == 0:
                    continue
                else:
                    (a,b) = backtrack.pop()
                    prev = (a,b)
            backtrack.append(prev)
            prev = (u,v)
            backtrack.append((u,v))
        else:
            prev = (u,v)
            backtrack.append((u,v))
    return blockingFlow

def augment_s_t_flow(graph, path):
    augmentFlow = path.set_all_cap(graph.get_min_cap())
    return augmentFlow

def generate_full_blocking_flow(graph, s, t):
    levelGraph = generate_level_graph(graph, s, t)
    return generate_blocking_flow(levelGraph, depth_first_search_with_levels(levelGraph, s, t), t)

def dinics(graph, s, t):
    residual = copy.deepcopy(graph)
    flow = Flow()

    while True:
        try:
            blockingFlow = generate_full_blocking_flow(residual, s, t)
            if len(blockingFlow.get_values()) != 0:
                flow -= blockingFlow
                residual += blockingFlow
            else:
                break
        except:
            break
    
    print("graph: "); print(graph)
    print("flow: "); print(flow)

    maxFlow = 0
    for nbr in flow.getNbrs(s):
        maxFlow += flow[s,nbr]

    return maxFlow