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

1. Rank features by their variance.
    1. Group articles by their feature characteristics. Eg.

    | feature          | weeks on sale | revenue |
    |------------------|---------------|---------|
    | characteristic A | 1             | 10      |
    |                  | 2             | 20      |
    |                  | 3             | 25      |
    | characteristic B | 1             | 5       |
    |                  | 2             | 10      |
    |                  | 3             | 15      |
    | ...              | ...           | ...     |

    2. Determine inter- and intra-feature variance of each feature.
    3. Calculate a *Score* of these measures to rank each feature by its importance.
2. For every feature in descending order of their importance:
    1. Determine which combination of characteristics could be grouped together (low variance) and which should form separate clusters (high variance)
    2. Identify existing clusters, to group these sets of characteristics with
       or form new ones. (Divide existing clusters)
3. Calculate a measure which determines the _Cluster Fit_
4.




