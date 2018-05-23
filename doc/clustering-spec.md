# Specification of the tailor Clustering Algorithm
## Goal
The clustering algorithm should assign every existing article of the dataset to
a cluster, based on the historical data of its revenue or sold articles.
Clusters should be formed through the combination of characteristics of the
article. E.g.
- Cluster 1: _Brand_ = [Fimmilena, Almaviahenae], _Color_ = [himmelgrau], _Season_ = [Sommer]
- Cluster 2: _Brand_ = [Baudihillia, Lodur, Tuisto], _Color_ = [gold, graublau,
  khaki], _Season_ = [Winter]
- ...

The variance (of the e.g. revenue curve) within the clusters should be as low as
possible, while the clusters themselves should be as big as possible to form a
valid population for further analysis.

## Outline of the Algorithm

1. *Rank features* by their variance.
    1. Group articles by their feature characteristics.

    _Example:_

    | feature          | weeks on sale | revenue |
    |------------------|---------------|---------|
    | characteristic A | 1             | 10      |
    |                  | 2             | 20      |
    |                  | ..            | ..      |
    | characteristic B | 1             | 5       |
    |                  | 2             | 10      |
    |                  | ..            | ..      |
    | characteristic C | 1             | 7       |
    | ...              | ...           | ...     |

    2. Determine inter- and intra-feature variance of each feature.
    3. Calculate a *Score* of these measures to rank each feature by its importance.
2. Clustering: For every feature `f` in descending order of their *Score*:
    1. Determine which combination of characteristics could be grouped together (low variance) and which should form separate clusters (high variance)
    2. If `f` is the first feature:
    Use this combinations of characteristics to form clusters.

    _Example:_

    | Cluster | color       |
    |---------|-------------|
    | 1       | red         |
    | 2       | green       |
    | 3       | blue, white |

    3. Else:
    For every existing cluster `c`: Split `c` by each characteristic of `f` and
    determine which of these "sub-clusters" can be unified again.

    _Example:_

    | Cluster | color       | brand  |
    |---------|-------------|--------|
    | 1       | red         | adidas |
    | 2       | red         | puma   |
    | 3       | green       | adidas |
    | 4       | green       | puma   |
    | 5       | blue, white | adidas |
    | 6       | blue, white | puma   |

    Unify similar (sub-)clusters using the variance/distance measure again:

    | Cluster | color       | brand        |
    |---------|-------------|--------------|
    | 1       | red         | adidas, puma |
    | 2       | green       | adidas       |
    | 3       | green       | puma         |
    | 4       | blue, white | adidas, puma |


3. *Evaluate the quality* of the cluster using measure which determines the _Cluster Fit_ or _Cluster Goodness_.
4. Determine the *best possible clustering* by using the number of features in
   `2.` which has the highest Quality in `3`.

### Alternative to `2.`:
Use every combination of the _x_ highest scored features
and calculate distance between every subset and then combine close subsets to clusters.
