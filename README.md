# Multimatching

A Python package for computing the bottleneck distance between persistence diagrams.
It is optimized for diagrams in which the points have multiplicity.

## Basic explanation of algorithm

The basic pattern for the algorithm resembles the approach in the `persim` package.
Instead of using the Hopcroft-Karp algorithm to check for a perfect matching at a given scale, we instead solve a maximum flow problem where the capacities are determined by the multiplicities.

Steps:
- We first compute the pairwise distances between points, adding a dummy point to each set for the diagonal.
- Then, we do a binary search for the bottleneck distance.  At each scale $\delta$ , we do the following
  - Construct a $\delta$-neighborhood graph.
  - We create a dummy sink and source vertex
  - Create edges from source to points in diagram A
  - Create edges from source to points in diagram B
  - Add edges with the diagonal such as: sink, source, and diagonal to diagonal
  - For all edges, the capacity is the minimum multiplicity of the endpoints.
  - Compute a maximum flow in the graph.
  - If the total flow corresponds to the total multiplicity of the diagrams, then we search try a smaller scale. Otherwise, we try a larger scale.

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
