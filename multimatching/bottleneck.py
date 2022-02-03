from collections import namedtuple
from ortools.graph import pywrapgraph
from pdsketch import Diagram


def dB(A: Diagram, B: Diagram, upperbound=float('inf'), get_matching=False) -> float:
    n_A = sum(A.mass.values())
    n_B = sum(B.mass.values())
    n = len(A) + 1
    diag_A = len(A)
    diag_B = len(A) + len(B) + 1
    source = diag_B + 1
    sink = source + 1
    expected_flow = n_A + n_B

    edges = []
    Edge = namedtuple('Edge', ['distance', 'start', 'end', 'capacity'])
    for i, (a, m) in enumerate(A.mass.items()):
        # add edge from source to points in A
        edges.append(Edge(0, source, i, m))
        # add edge from each point to the diagonal
        edges.append(Edge(a.l_inf_dist(a.diagproj()), i, diag_B, m))
    # Next, add the edges from B to the sink.
    for j, (b, m) in enumerate(B.mass.items(), start=n):
        # add edges to from points to the sink
        edges.append(Edge(0, j, sink, m))
        # add edges from diagonal to the points
        edges.append(Edge(b.l_inf_dist(b.diagproj()), diag_A, j, m))
    # Add edges with the diagonal.
    edges.append(Edge(0, diag_A, diag_B, min(n_A, n_B)))
    edges.append(Edge(0, source, diag_A, n_B))
    edges.append(Edge(0, diag_B, sink, n_A))
    # Only include the edges from A to B that might be matched.
    for i, (a, a_mass) in enumerate(A.mass.items()):
        for j, (b, b_mass) in enumerate(B.mass.items(), start=n):
            if a.pp_dist(b) <= min(upperbound, max(a.l_inf_dist(a.diagproj()), b.l_inf_dist(b.diagproj()))):
                edges.append(Edge(a.dist(b), i, j, min(a_mass, b_mass)))
    # Sort the eges by length
    edges.sort()

    # Binary search over the edges for the bottleneck distance.
    bottleneck = Edge(float('inf'), None, None, None)
    i, j = 0, len(edges)
    while j - i > 1:
        mid = (i + j) // 2
        # Build the graph
        G = pywrapgraph.SimpleMaxFlow()
        for edgeindex, edge in enumerate(edges):
            if edgeindex > mid:
                break
            G.AddArcWithCapacity(edge.start, edge.end, edge.capacity)

        # Compute the Maxflow
        G.Solve(source, sink)
        if G.OptimalFlow() == expected_flow:
            bottleneck = edges[mid]
            maxflow = G
            i, j = i, mid
        else:
            i, j = mid, j

    tp = {}
    if get_matching:
        for i in range(maxflow.NumArcs()):
            a_index = maxflow.Tail(i)
            b_index = maxflow.Head(i)
            if (a_index != source and b_index != sink):
                if a_index in tp and b_index in tp[a_index]:
                        tp[a_index][b_index] += maxflow.Flow(i)
                else:
                    tp[a_index] = {b_index: maxflow.Flow(i)}
        return bottleneck.distance, tp
    else:
        return bottleneck.distance
