# Pigment

[![License: ISC][isc_shield]][isc_link]
[![CC BY-SA 4.0][cc-by-shield]][cc-by]

The problem of splitting up a skincare regime into partitions such that each
partition does not interfere with itself is equivalent to the
[minimal clique cover problem][clique_cover_wp], which can be transformed into
the [vertex colouring of a graph][graph_colour_wp], both of which are NP-hard
and thus computationally infeasible to find optimal solutions for. This project
is a brute-force proof-of-concept that exhaustively solves the problem of good
skincare product grouping!

## Usage

1. Modify the ingredient conflict dictionary (named `CONFLICTS` in the
   `pigment.py` mainline) to reflect your skincare products. If you say `A`
   conflicts with `B`, you don't have to also write the rule that `B` conflicts
   with `A`. The script handles the reflexivity.

2. Run the program (you need Python 3):

   ```bash
   python3 pigment.py
   ```

## Algorithm

This algorithm takes in an adjacency list for a conflict graph where each edge
between two nodes represents an instance of two ingredients conflicting.

It then exhaustively generates every possible partition using a recursive
backtracking depth-first-search algorithm where for each ingredient, it
explores every sub-tree consisting of adding the ingredient to every existing
partition before finally creating a new partition. Each terminal/leaf node
represents a generated group of partitions, which we exhaustively check: for
each partition in the group, we check to see if any pair exists as an edge in
the conflict dictionary. If no such pairs exist among any partition, the group
is valid.

![partition tree](resources/partitions.svg)

The algorithm looks for the valid group with the least amount of partitions.

The number of groups that are brute-force generated is equivalent to the
_n_<sup>th</sup> [Bell number][bell_number_wp] and it is sequence
[A000110][num_seq] in the OEIS.

It runs in _O(a fuckton of time)_. If you have a lot of stuff in your skincare
routine, this algorithm may take forever to run. It is recommended that you do
not add vanity elements (aka adding an element just for it to show up in the
final result) such as:

```python
CONFLICTS = OrderedDict((
    ("A", ["B", "C"])
    ("D", [])
))
```

In this case, `"D"` is a vanity element; it contributes nothing to conflict
data but bloats the state space (which, in a brute-force algorithm like this,
is not good). If an element doesn't conflict with anything, then use it as
liberally as you like without restriction.

You have been warned.

## Modelling

Say, for the purposes of illustration (as these opinions are still hotly
debated in the skincare community today), we have the following ingredients:

- Retinol
- AHAs/BHAs
- Copper peptides
- Ferrulic acid

and the following interactions:

- Retinol and AHAs/BHAs conflict with each other
- Copper peptides interfere with AHAs/BHAs
- Ferrulic acid interferes with copper peptides

We can therefore model compatible products as an undirected graph where each
node represents a skincare ingredient and each edge between node _a_ and node
_b_ represents the sentence "ingredient _a_ is compatible with ingredient _b_".
We can represent the relation above as such:

![compatibility graph](resources/compat_graph.svg)

The ideal here is that we want to take all four of these ingredients at once,
however as noted by the conflicts above, that isn't possible. The next best
solution, if we can't create 1 group, is to try to create 2 groups. We know
that in our model, retinol is compatible with copper peptides, and ferrulic
acid is compatible with AHAs/BHAs, so we discard the possibility of using
retinol with ferrulic acid (as the group potentially containing ferrulic acid)
contains AHAs/BHAs, which are incompatible with retinol, as shown by the lack
of edge.

![minimum clique](resources/min_clique.svg)

This is the optimal solution. In one skincare session, we take retinol with the
copper peptides, and another session we take AHAs/BHAs and ferrulic acid.

Our overarching goal, therefore, is to divide the ingredients list into as few
groups as possible such that each group's ingredients represents a clique,
where a clique is an induced subgraph that is complete. In layperson's terms,
we are looking to create subgraphs of ingredients such that each ingredient has
an edge connected to every other ingredient node in the subgraph. Such complete
subgraphs are known as cliques. As shown below, when two ingredients are
compatible with each other, the resultant clique has a single edge between two
nodes (as shown by _K<sub>2</sub>: 1_). For four ingredients, the resultant
clique has six edges between the four nodes (as shown by _K<sub>2</sub>:6_). To
see ten ingredients compatible with each other is somewhat uncommon.

![complete graphs](resources/complete_graphs.png)
_These images are taken from Wikipedia.org and are by koko90. See
[attribution](#Attribution) for details_

## Minimal Clique Cover

In formal terms, a "clique cover" or "partition into cliques" of an undirected
graph is a partition (or splitting of the graph into groups) into constituent
cliques. Our problem is to find the "**minimal**" clique cover—aka—doing it in
the least number of cliques—or splits—possible. As shown in the figure above,
the trivial case is _K<sub>1</sub>: 0_ as each individual ingredient is its own
clique, but that's the worst-case scenario we are trying to avoid. It would
mean that no skincare ingredient is compatible with anything else e.g. you
may have to take each 10 skincare ingredient on separate days, which would be a
scheduling nightmare.

## Graph Colouring

We can make things more readable by looking at an equivalent problem.

Given a graph _G_, the complement of the graph, let's call it _G2_, is a graph
with the same nodes as _G_, but every edge in the original graph is missing,
and every midding edge in the original graph is now an edge. In layperson's
terms, a complement graph _G2_ for graph _G_ contains only the edges necessary
to turn _G_ into a complete graph, as shown by this diagram:

![complement of the Petersen graph](resources/comp_petersen.jpg)
_Image edited by Claudio Rocchini; derived from David Eppstein. See
[attribution](#Attribution) for details_

We can invert the "maximal clique" problem by not mapping whether two skincare
products are compatible with each other, but rather if they conflict. This
makes specifications a whole lot easier to make, as now we can assume anything
that isn't connected by an edge is compatible. If we change our first graph to
model conflicts instead of synergies, we get the following:

![conflict graph](resources/conflict_graph.svg)

Our problem is now to induce subgraphs such that none of the nodes have any
edges between them. Each subgraph is its own group. In this example, we induce
the subgraphs for the nodes {`Retinol`, `Copper peptides`} as well as for
{`Ferrulic acid`, `AHAs/BHAs`}, as each graph has no nodes:

![coloured conflict graph](resources/coloured_conflicts.svg)

Those with a background in CS will immediately notice that this is actually the
well-studied graph colouring sub-problem known as "vertex colouring": colouring
a graph such that no two colours are adjacent to each other. In this case, each
colour group represents a partition, like from earlier. Again, the optimization
problem is NP-hard and is intractable. Which is why the algorithm solves the
colouring problem in the ugliest, most brute force way possible.

## Bibliography

- <https://en.wikipedia.org/wiki/Clique_cover>

- <https://en.wikipedia.org/wiki/Complement_graph>

- <https://en.wikipedia.org/wiki/Bell_number>

- <https://en.wikipedia.org/wiki/Graph_coloring>

## Attribution

- Graphs made by me using [Dreampuf's Dot Grapher][gv_link] and they are
  licensed as [CC BY-SA 4.0][cc-by] as the project is
- Complete graphs [K1][k1_link], [K2][k2_link], and [K3][k3_link] are simple
  geometry and thus are in the public domain (author is David Benbennick).
- Simplex graphs [4][s_4], [5][s_5], [6][s_6], [7][s_7], [8][s_8], [9][s_9],
  [10][s_10], [11][s_11], were released by Koko90 under [GFDL][gfdl] and
  [CC BY-SA 3.0][cc_by_sa_3_0] and will be coalesced into the license of this
  project, thus making them [CC BY-SA 4.0][cc-by]
- The Petersen graph complement image was edited by Claudio Rocchini whose
  original author was David Eppstein, also released under [GFDL][gfdl] and
  [CC BY-SA 3.0][cc_by_sa_3_0]. [CC BY-SA 4.0][cc-by] as per the project.

[isc_shield]: https://img.shields.io/badge/License-ISC-blue.svg
[isc_link]: https://opensource.org/licenses/ISC
[cc-by]: https://creativecommons.org/licenses/by-sa/4.0/
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
[clique_cover_wp]: https://en.wikipedia.org/wiki/Clique_cover
[graph_colour_wp]: https://en.wikipedia.org/wiki/Graph_coloring#Vertex_coloring
[bell_number_wp]: https://en.wikipedia.org/wiki/Bell_number
[num_seq]: https://oeis.org/A000110
[gv_link]: https://dreampuf.github.io/GraphvizOnline/
[k1_link]: https://en.wikipedia.org/wiki/File:Complete_graph_K1.svg
[k2_link]: https://en.wikipedia.org/wiki/File:Complete_graph_K2.svg
[k3_link]: https://en.wikipedia.org/wiki/File:Complete_graph_K3.svg
[gfdl]: https://www.gnu.org/licenses/fdl-1.3.html
[s_4]: https://en.wikipedia.org/wiki/File:4-simplex_graph.svg
[s_5]: https://en.wikipedia.org/wiki/File:5-simplex_graph.svg
[s_6]: https://en.wikipedia.org/wiki/File:6-simplex_graph.svg
[s_7]: https://en.wikipedia.org/wiki/File:7-simplex_graph.svg
[s_8]: https://en.wikipedia.org/wiki/File:8-simplex_graph.svg
[s_9]: https://en.wikipedia.org/wiki/File:9-simplex_graph.svg
[s_10]: https://en.wikipedia.org/wiki/File:10-simplex_graph.svg
[s_11]: https://en.wikipedia.org/wiki/File:11-simplex_graph.svg
[cc_by_sa_3_0]: https://creativecommons.org/licenses/by-sa/3.0/deed.en
