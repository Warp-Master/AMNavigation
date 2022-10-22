from collections import namedtuple

Edge = namedtuple("Edge", ("id", "to", "len"))
Graph = dict[int, list]
NameMap = dict[str, int]
DistanceMap = dict[int, float]
PathMap = dict[int, int]
Cache = dict[int, tuple[DistanceMap, PathMap]]
