from collections import namedtuple

from ortools.graph import pywrapgraph
from pdsketch import Diagram


def dB(A: Diagram, B: Diagram, upperbound=float('inf')) -> float:
    list_A = A.get_point_mass_lists()[0]
    list_B = B.get_point_mass_lists()[0]
    n_A = sum(1 for a in list_A)
    n_B = sum(1 for a in list_B)
    n = len(list_A)
    diag_A = len(list_A)
    diag_B = len(list_A) + len(list_B) + 1
    source = diag_B + 1
    sink = source + 1
    expected_flow = n_A + n_B

    edges = []
    Edge = namedtuple('Edge', ['distance', 'start', 'end', 'capacity'])
    for i, a in enumerate(list_A):
        # add edge from source to points in A
        edges.append(Edge(0, source, i, 1))
        # add edge from
        edges.append(Edge(a.l_inf_dist(a.diagproj()), i, diag_B, 1))
    # Next, add the edges from B to the sink.
    for j, b in enumerate(B, start=n):
        edges.append(Edge(0, j, sink, 1))
        edges.append(Edge(b.l_inf_dist(b.diagproj()), diag_A, j, 1))
    # Add edges with the diagonal.
    edges.append(Edge(0, diag_A, diag_B, min(n_A, n_B)))
    edges.append(Edge(0, source, diag_A, n_B))
    edges.append(Edge(0, diag_B, sink, n_A))
    # Only include the edges from A to B that might be matched.
    for i, a in enumerate(A):
        for j, b in enumerate(B, start=n):
            if a.pp_dist(b) <= min(upperbound, max(a.l_inf_dist(a.diagproj()), b.l_inf_dist(b.diagproj(

            )))):
                edges.append(Edge(a.dist(b), i, j, 1))
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
            i, j = i, mid
        else:
            i, j = mid, j

    return bottleneck.distance
