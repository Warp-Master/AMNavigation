from dijkstra import dijkstra
from MyTypes import Graph, NameMap, Cache


def add_to_cache(name: str, cache: Cache, graph: Graph, name_mapping: NameMap) -> None:
    """Функция добавления в кеш"""
    terminal_id = name_mapping[name]
    distance_map = dijkstra(graph, terminal_id)
    cache[terminal_id] = distance_map
