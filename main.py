"""
Todo:
    - move DBWorker creation to main
"""
from collections import defaultdict
from datetime import timedelta, datetime

from bus_gens import small_bus_gen, big_bus_gen
from cache import add_to_cache
from cls.Bus import BusPool
from cls.Task import Task, TaskStatus
from config import PRECACHED_LOCATION_LIST
from config import SPEED_LIMIT, LOAD_TIME, UNLOAD_TIME
from db import database
from parser import build_graph, parse_flights, parse_naming_map


def main():
    cache = defaultdict(None)

    naming_map = parse_naming_map("csv/name-map.csv")
    graph = build_graph("csv/edges.csv")
    flights = sorted(parse_flights("csv/timetable.csv"))

    bus_pool = BusPool(list(small_bus_gen()), list(big_bus_gen()))

    for terminal_name in PRECACHED_LOCATION_LIST:
        add_to_cache(terminal_name, cache, graph, naming_map)

    now = datetime.now()  # this should be changed to generated time in modulation

    database.execute("DELETE FROM Task;", commit=True)
    for flight in flights:
        if flight.type == 'A':
            start_id = naming_map[flight.parking_number]
        elif flight.type == 'D':
            start_id = naming_map[flight.gate_number]
        else:
            raise ValueError(f"bad flight type {flight.type}")

        solution = bus_pool.get_optimal_task_sol(now,
                                                 graph,
                                                 cache,
                                                 flight.passengers_count,
                                                 start_id)

        secs_for_exec = flight.get_distance(graph, cache, naming_map) * 2 / SPEED_LIMIT + UNLOAD_TIME + LOAD_TIME
        time_for_done = solution[0] + timedelta(seconds=secs_for_exec)

        Task(
            id=None,
            flight=flight,
            status=TaskStatus.PLANNED,
            start_time=now + solution[0],
            finish_time=now + time_for_done,
            bus_list=solution[1] + solution[2]
        ).write_to_db(database, commit=True)

        print(f"{flight}\t{time_for_done}")
    else:
        database.commit()
    # debug section
    # print(name_mapping)
    # print(*graph.items(), sep="\n")


if __name__ == "__main__":
    main()
