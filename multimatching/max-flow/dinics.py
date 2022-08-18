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
    prevIdx, idx = [0, 1]
    while idx < len(path):
        prev = path[prevIdx]; curr = path[idx]
        (prevU, prevV) = prev; (currU, currV) = curr
        if prevV == currU:
            currentPath.addedge(curr, levelgraph[curr])
            if currV == t:
                currentPath.set_all_cap(currentPath.get_min_cap())
                blockingFlow += currentPath
                levelgraph -= currentPath
                currentPath.reset_cap(levelgraph)
            idx += 1; prevIdx = idx - 1
        else:
            try:
                currentPath.removeedge(prev)
            except:
                pass
            prevIdx -= 1
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
                flow += blockingFlow
                residual -= blockingFlow
            else:
                break
        except:
            break

    maxFlow = 0
    for nbr in flow.getNbrs(s):
        maxFlow += flow[s,nbr]

    return maxFlow