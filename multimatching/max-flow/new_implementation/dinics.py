from graph import Graph
from flow import Flow
import copy
import math

def generate_level_graph(graph, s, t):
    Q = [(None, s)]
    levels = Graph()
    while Q:
        (prev,v) = Q.pop(0)
        if v not in levels:
            levels[prev,v] = graph[prev,v]
            if v != t:
                for nbr in graph.getNbrs(v):
                    if graph[v, nbr] > 0:
                        Q.append((v,nbr))
    return levels

def depth_first_search_with_levels(levelgraph, s, t):
    S = [(None, s)] 
    path = []
    while S:
        current = S.pop()
        v = current[1]
        if v not in path:
            path.append(v)
            if v == t:
                continue
            for nbr in levelgraph.getNbrs(v):
                if nbr not in path:
                    S.append((v,nbr))
    path.append(t)
    return path

def generate_blocking_flow(levelgraph, path, t):
    blockingFlow = Flow()
    currentPath = []
    prev = path.pop(0)
    while path:
        curr = path.pop(0)
        currentPath.append((prev, curr))
        if curr != t:
            prev = curr
        else:
            blockingFlow += augment_s_t_flow(levelgraph, currentPath)
            currentPath.clear()
    return blockingFlow

def augment_s_t_flow(graph, path):
    flow = Flow()
    minCap = float('Inf')
    for e in path:
        currCap = graph[e]
        flow.addedge(e, 0)
        if currCap < minCap:
            minCap = currCap
    flow.set_all_cap(minCap)
    return flow

def generate_full_blocking_flow(graph, s, t):
    return generate_blocking_flow(graph, depth_first_search_with_levels(generate_level_graph(graph, s, t), s, t), t)

def dinics(graph, s, t):
    residual = copy.deepcopy(graph)
    flow = Flow()

    while True:
        try:
            blockingFlow = generate_full_blocking_flow(residual, s, t)
            flow += blockingFlow
            residual -= blockingFlow
        except:
            break
    
    print(flow)