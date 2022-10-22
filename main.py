from parser import build_graph, parse_flights, parse_naming_map
from constants import PRECACHED_LOCATION_LIST
from cache_terminal import cache_terminal
from collections import defaultdict


def main():
    terminal_cache = defaultdict(None)

    naming_map = parse_naming_map("csv/name-map.csv")
    graph = build_graph("csv/edges.csv")
    flights = parse_flights("csv/timetable.csv")

    for terminal_name in PRECACHED_LOCATION_LIST:
        cache_terminal(terminal_name, terminal_cache, graph, naming_map)

    for flight in flights:
        print(flight.get_distance(graph, terminal_cache, naming_map))

    # debug section
    # print(name_mapping)
    # print(*graph.items(), sep="\n")


if __name__ == "__main__":
    main()
