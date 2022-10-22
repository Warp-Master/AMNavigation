from collections import defaultdict
from typing import Iterator

from Bus import Bus, BusStatus
from User import User, Group
from cache import add_to_cache
from config import PRECACHED_LOCATION_LIST
from config import SMALL_BUS_CNT, SMALL_BUS_CAPACITY, BIG_BUS_CNT, BIG_BUS_CAPACITY, SPEED_LIMIT, LOAD_TIME, UNLOAD_TIME
from parser import build_graph, parse_flights, parse_naming_map
from copy import copy
import heapq


# import asyncio
# from asyncio.queues import PriorityQueue


def init_bus_generator() -> Iterator[Bus]:
    u = User(
                id=0,
                login="",
                pwd_hash="",
                salt="",
                group=Group.VIEWER,
                name=""
    )

    for i in range(SMALL_BUS_CNT):
        yield Bus(
            id=i,
            task=None,
            driver=copy(u),
            capacity=SMALL_BUS_CAPACITY,
            status=BusStatus.WAITING,
            location_id=159,
            free_location_id=None,
            free_time=None,
        )
    for i in range(BIG_BUS_CNT):
        yield Bus(
            id=SMALL_BUS_CNT + i,
            task=None,
            driver=copy(u),
            capacity=BIG_BUS_CAPACITY,
            status=BusStatus.WAITING,
            location_id=159,
            free_location_id=None,
            free_time=None,
        )


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
