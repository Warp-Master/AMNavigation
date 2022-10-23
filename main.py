from collections import defaultdict
from copy import copy
from datetime import timedelta, datetime
from operator import methodcaller, itemgetter
from typing import Iterator

from Bus import Bus, BusStatus
from MyTypes import Graph, Cache, TaskSolution
from User import User, Group
from cache import add_to_cache
from config import PRECACHED_LOCATION_LIST
from config import SMALL_BUS_CNT, SMALL_BUS_CAPACITY, BIG_BUS_CNT, BIG_BUS_CAPACITY
from parser import build_graph, parse_flights, parse_naming_map


class BusPool:
    def __init__(self, small_busses: list, big_busses: list):
        self.small_buses = small_busses
        self.big_buses = big_busses

    def get_optimal_task_sol(self, start_time: datetime, graph: Graph,
                             cache: Cache, pass_cnt: int, target_id: int) -> TaskSolution:
        """Возвращает наилучшее время, чтобы доставить нужное кол-во машин в target_id и списки необходимых автобусов"""
        get_time = methodcaller("time_for_delivery", start_time, graph, cache, target_id)
        sorted_small = sorted(zip(map(get_time, self.small_buses), self.small_buses), key=itemgetter(0))
        sorted_big = sorted(zip(map(get_time, self.big_buses), self.big_buses), key=itemgetter(0))

        best_solution = (timedelta.max, 0, 0)
        for big_cnt in range(pass_cnt // 100 + pass_cnt % 100 > 0 + 1):
            if big_cnt > pass_cnt // 100:
                sml_cnt = 0
            else:
                remaining_pass = (pass_cnt - 100 * big_cnt)
                sml_cnt = remaining_pass // 50 + remaining_pass % 50 > 0
            needed_time = max(sorted_small[sml_cnt - 1][0], sorted_big[big_cnt - 1][0])
            if needed_time < best_solution[0]:
                best_solution = (needed_time, sml_cnt, big_cnt)

        return (best_solution[0],
                list(map(itemgetter(1), sorted_small[:best_solution[1] - 1])),
                list(map(itemgetter(1), sorted_big[:best_solution[2] - 1])))


def small_bus_gen():
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


def big_bus_gen():
    u = User(
        id=0,
        login="",
        pwd_hash="",
        salt="",
        group=Group.VIEWER,
        name=""
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


def init_bus_generator() -> Iterator[Bus]:
    yield from small_bus_gen()
    yield from big_bus_gen()


def main():
    cache = defaultdict(None)

    naming_map = parse_naming_map("csv/name-map.csv")
    graph = build_graph("csv/edges.csv")
    flights = sorted(parse_flights("csv/timetable.csv"))

    bus_pool = BusPool(list(small_bus_gen()), list(big_bus_gen()))

    for terminal_name in PRECACHED_LOCATION_LIST:
        add_to_cache(terminal_name, cache, graph, naming_map)

    now = datetime.now()
    for flight in flights:
        if flight.type == 'A':
            start_id = naming_map[flight.parking_number]
        elif flight.type == 'D':
            start_id = naming_map[flight.gate_number]
        else:
            raise ValueError(f"bad flight type {flight.type}")

        solution: TaskSolution = bus_pool.get_optimal_task_sol(now,
                                                               graph,
                                                               cache,
                                                               flight.passengers_count,
                                                               start_id)
        print(f"{flight}\t{solution}")

    # while True:
    #     ...
    # debug section
    # print(name_mapping)
    # print(*graph.items(), sep="\n")


if __name__ == "__main__":
    main()
