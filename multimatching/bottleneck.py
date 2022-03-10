from collections import namedtuple, defaultdict

from ortools.graph import pywrapgraph
from pdsketch import Diagram, PDPoint


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
    b_diagram_offset = len(A) + 1
    diagonal_A = len(A)
    diagonal_B = len(A) + len(B) + 1
    source = diagonal_B + 1
    sink = source + 1
    expected_flow = n_A + n_B
    edges = []
    Edge = namedtuple('Edge', ['distance', 'start', 'end', 'capacity'])
    diagonal_PDpoint = PDPoint((0, 0))
    points = []

    for i, (a, m) in enumerate(A.mass.items()):
        # add edge from source to points in A
        edges.append(Edge(0, source, i, m))
        # add edge from each point to the diagonal
        edges.append(Edge(a.l_inf_dist(a.diagproj()), i, diagonal_B, m))
        points.append(a)

    points.append(diagonal_PDpoint)

    # Next, add the edges from B to the sink.
    for j, (b, m) in enumerate(B.mass.items(), start=b_diagram_offset):
        # add edges to from points to the sink
        edges.append(Edge(0, j, sink, m))
        # add edges from diagonal to the points
        edges.append(Edge(b.l_inf_dist(b.diagproj()), diagonal_A, j, m))
        points.append(b)

    points.append(diagonal_PDpoint)

    # Add edges with the diagonal.
    edges.append(Edge(0, diagonal_A, diagonal_B, min(n_A, n_B)))
    edges.append(Edge(0, source, diagonal_A, n_B))
    edges.append(Edge(0, diagonal_B, sink, n_A))

    # Only include the edges from A to B that might be matched.
    for i, (a, a_mass) in enumerate(A.mass.items()):
        for j, (b, b_mass) in enumerate(B.mass.items(), start=b_diagram_offset):
            a_distance_to_diagonal = a.l_inf_dist(a.diagproj())
            b_distance_to_diagonal = b.l_inf_dist(b.diagproj())
            # we want the longer distance:
            # if either has a shorter distance to the diagonal then we'd like to match with the
            # diagonal instead of the other point
            longest_diagonal_distance = max(a_distance_to_diagonal, b_distance_to_diagonal)
            # upperbound is the hint that the user potentially gave us to decrease the size of
            # the search space
            comparedDist = min(upperbound, longest_diagonal_distance)
            if a.pp_dist(b) <= comparedDist:
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
    tp = defaultdict(dict)
    if get_matching:
        for i in range(maxflow.NumArcs()):
            tail_index = maxflow.Tail(i)
            head_index = maxflow.Head(i)
            if tail_index != source and head_index != sink and maxflow.Flow(i) > 0:
                tp[points[tail_index]][points[head_index]] = maxflow.Flow(i)
        return bottleneck.distance, tp
    else:
        return bottleneck.distance
