import heapq
from collections import defaultdict

from MyTypes import Graph, DistanceMap, Cache


def dijkstra(g: Graph, start: int, stop: int | None = None, cache: Cache | None = None) -> DistanceMap:
    if cache is not None and start in cache:
        return cache[start]

    distance = defaultdict(lambda: float("inf"))
    distance[start] = 0

    pq = [(0., start)]
    while pq:
        cur_d, v = heapq.heappop(pq)
        if v == stop:
            break
        if cur_d > distance[v]:
            continue

        for edge in g[v]:
            if distance[v] + edge.len < distance[edge.to]:
                distance[edge.to] = distance[v] + edge.len
                heapq.heappush(pq, (distance[edge.to], edge.to))
    return distance
