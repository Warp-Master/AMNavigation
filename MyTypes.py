from collections import namedtuple
from datetime import timedelta

# from Bus import Bus

Edge = namedtuple("Edge", ("id", "to", "len"))
Graph = dict[int, list]
NameMap = dict[str, int]
DistanceMap = dict[int, float]
Cache = dict[int, DistanceMap]
TaskSolution = tuple[timedelta, list["Bus"], list["Bus"]]
