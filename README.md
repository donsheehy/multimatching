# Multi Matching

A python package for computing the bottleneck distance between two persistence diagrams with
lots of duplicate points (multiplicity). This package uses the reduction of bipartite matching to
maximum flow to provide a speedup in cases with high multiplicities.

## Basic explanation of algorithm

We use the fact that bipartite matching can be reduced to maximum flow.

Steps:
- We create a dummy sink and source
- Create edges from source to points in diagram A
- Create edges from source to points in diagram B
- Add edges with the diagonal such as: sink, source, and diagonal to diagonal
- Create edges from points in diagram A to diagram B if they can be matched, i.e. if either of
  the points has a shorter distance to the diagonal then we'd like to match with the diagonal
  instead of the point
- Conduct binary search over the set of edges created based on bottleneck distance
- Each time we create a new matching, we check if it is a perfect matching using a maximum flow
  algorithm (we use the one from or-tools created by Google)

## Examples

### Example without multiplicity:

Diagram A with points (3, 6), (1, 2), (6, 18), (1, 3)

Diagram B with points (4, 6), (7, 21)

Output of bottleneck distance: 3.0

[//]: # (todo: grab pics from sid)

### Example with multiplicity:

Diagram A with point (0, 6), and multiplicity 1000000000

This means that there are 1000000000 copies of (0,6)

Diagram B with point (1, 6), and multiplicity 1000000000

Output of bottleneck distance: 1.0

[//]: # (todo: grab pics from sid)
