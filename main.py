from parser import build_graph, parse_flights, parse_naming_map
from config import PRECACHED_LOCATION_LIST
from cache import add_to_cache
from collections import defaultdict


def main():
    cache = defaultdict(None)

    naming_map = parse_naming_map("csv/name-map.csv")
    graph = build_graph("csv/edges.csv")
    flights = parse_flights("csv/timetable.csv")

    for terminal_name in PRECACHED_LOCATION_LIST:
        add_to_cache(terminal_name, cache, graph, naming_map)

    for flight in flights:
        print(flight, flight.get_distance(graph, cache, naming_map))

    # debug section
    # print(name_mapping)
    # print(*graph.items(), sep="\n")


if __name__ == "__main__":
    main()
