from collections import namedtuple

from ortools.graph import pywrapgraph
from pdsketch import Diagram


def dB(A: Diagram, B: Diagram, upperbound=float('inf'), get_matching=False) -> float:
    """

    :param A: Diagram from pdsketch of first PD
    :param B: Diagram from pdsketch of second PD
    :param upperbound: Default float('inf'). If the user knows that the distance is
    guaranteed to be below a certain distance then this would speed up the calculation.
    :param get_matching: Default False. If true, returns matching between the two PDs
    :return:

    bottleneck_distance: float
    matching: dict, returned if get_matching is set to true
    """
    n_A = sum(A.mass.values())
    n_B = sum(B.mass.values())
    n = len(A) + 1
    diagonal_A = len(A)
    diagonal_B = len(A) + len(B) + 1
    source = diagonal_B + 1
    sink = source + 1
    expected_flow = n_A + n_B
    edges = []
    Edge = namedtuple('Edge', ['distance', 'start', 'end', 'capacity'])
    A_point_mass_list = list()
    for i, (a, m) in enumerate(A.mass.items()):
        # add edge from source to points in A
        edges.append(Edge(0, source, i, m))
        # add edge from each point to the diagonal
        edges.append(Edge(a.l_inf_dist(a.diagproj()), i, diagonal_B, m))
        A_point_mass_list.append((a, m))
    # Next, add the edges from B to the sink.
    B_point_mass_list = list()
    for j, (b, m) in enumerate(B.mass.items(), start=n):
        # add edges to from points to the sink
        edges.append(Edge(0, j, sink, m))
        # add edges from diagonal to the points
        edges.append(Edge(b.l_inf_dist(b.diagproj()), diagonal_A, j, m))
        B_point_mass_list.append((b, m))
    # Add edges with the diagonal.
    edges.append(Edge(0, diagonal_A, diagonal_B, min(n_A, n_B)))
    edges.append(Edge(0, source, diagonal_A, n_B))
    edges.append(Edge(0, diagonal_B, sink, n_A))
    # Only include the edges from A to B that might be matched.
    for i, (a, a_mass) in enumerate(A.mass.items()):
        for j, (b, b_mass) in enumerate(B.mass.items(), start=n):
            if a.pp_dist(b) <= min(upperbound,
                                   max(a.l_inf_dist(a.diagproj()), b.l_inf_dist(b.diagproj()))):
                edges.append(Edge(a.dist(b), i, j, min(a_mass, b_mass)))
    # Sort the edges by length
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

    '''
    Format of TP:
        {point: {matched_point: number_matched}}
        
        Example: (0,1) with mass 2 is matched with (0,1) and the diagonal
                    {(0,1): {(0,1): 1, 'diag': 1}
    '''
    tp = {}
    # A_point_mass_list = list(A.mass)
    if get_matching:
        for i in range(maxflow.NumArcs()):
            tail_index = maxflow.Tail(i)
            head_index = maxflow.Head(i)
            if tail_index != source and head_index != sink:
                assert head_index > n-1
                assert tail_index < n

                tail_index = index_to_point_mapper(diagonal_A,
                                                   diagonal_B,
                                                   tail_index,
                                                   n,
                                                   A_point_mass_list,
                                                   B_point_mass_list)
                head_index = index_to_point_mapper(diagonal_A,
                                                   diagonal_B,
                                                   head_index,
                                                   n,
                                                   A_point_mass_list,
                                                   B_point_mass_list)
                if tail_index in tp and head_index in tp[tail_index]:
                    tp[tail_index][head_index] += maxflow.Flow(i)
                else:
                    tp[tail_index] = {head_index: maxflow.Flow(i)}
        return bottleneck.distance, tp
    else:
        return bottleneck.distance


def index_to_point_mapper(diag_A, diag_B, index, diagram_B_offset, A_point_mass_list,
                          B_point_mass_list):
    if index == diag_A or index == diag_B:
        index = 'diag'
    elif index < diag_A:
        index = A_point_mass_list[0][index]
    else:
        index = B_point_mass_list[0][index - diagram_B_offset]
    return index
