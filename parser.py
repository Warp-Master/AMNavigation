import sqlite3
from collections import defaultdict
from datetime import datetime

import csv
from Bus import Bus
from Flight import Flight
from MyTypes import NameMap, Graph, Edge
from Task import Task
from User import User


def parse_naming_map(filepath: str) -> NameMap:
    name_mapping = dict()
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # skip header
        for row in reader:
            name_mapping[row[1]] = int(row[0])
    return name_mapping


def build_graph(filepath: str) -> Graph:
    graph = defaultdict(list)

    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # skip header
        for row in reader:  # make directed graph
            edge_id = int(row[0])
            source = int(row[1])
            target = int(row[2])
            distance = int(row[3])
            graph[source].append(Edge(edge_id, target, distance))
    return graph


def parse_flights(filepath: str) -> list[Flight]:
    flights = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # skip header
        for row in reader:
            flight = Flight(
                flight_id=len(flights),
                date=datetime.strptime(f"{row[0]} {row[5]}", "%d.%m.%Y %H:%M"),
                flight_type=row[1],
                terminal_name=row[2],
                airline_code=row[3],
                airline_number=int(row[4]),
                airport_code=row[6],
                airport_name=row[7],
                aircraft_type=row[8],
                parking_number=row[9],
                gate_number=row[10],
                passengers_count=int(row[11]),
            )
            flights.append(flight)
    return flights


def load_db():
    conn = sqlite3.connect('bot_db.sqlite')
    cur = conn.cursor()

    index_flights = dict()
    index_tasks = dict()
    index_buses = dict()
    index_users = dict()

    cur.execute("SELECT * FROM \"User\"")
    for row in cur.fetchall():
        index_users[row[0]] = User(row[0], row[1], row[2], row[3], row[4], row[5])

    cur.execute("SELECT * FROM Flight")
    for row in cur.fetchall():
        index_flights[row[0]] = Flight(row[0], datetime.strptime(f"{row[1]}", "%Y-%m-%d %H:%M:%S"),
                                       row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])

    cur.execute("SELECT * FROM Task")
    for row in cur.fetchall():
        flight = index_flights[row[1]]
        index_tasks[row[0]] = Task(row[0], flight, row[2], datetime.strptime(f"{row[3]}", "%H:%M"),
                                   datetime.strptime(f"{row[4]}", "%H:%M"), [])

    cur.execute("SELECT * FROM Bus")
    for row in cur.fetchall():
        user = index_users[row[2]]
        if row[1] == 0:
            task = None
        else:
            task = index_tasks[row[1]]
        index_buses[row[0]] = Bus(row[0], task, user, row[3], row[4], row[5], row[6],
                                  datetime.strptime(f"{row[7]}", "%H:%M"))
        task.bus_list.append(index_buses[row[0]])

    conn.commit()
    conn.close()

    return (list(index_buses.values()),
            list(index_flights.values()),
            list(index_tasks.values()),
            list(index_users.values()))


if __name__ == "__main__":
    # For test
    conn = sqlite3.connect('bot_db.sqlite')
    cur = conn.cursor()
    # cur.execute("INSERT INTO User\
    #    (login, pwd_hash, salt, group_id, name)\
    #     VALUES ('l1', 'p1', 's1', 1, 'n1')")
    # cur.execute("INSERT INTO Task\
    #    (flight_id, status, load_time, unload_time)\
    #     VALUES (1, 's1', '01:15', '01:55')")
    # cur.execute("INSERT INTO Bus\
    #    (current_task_id, driver_id, capacity, status, location_id, free_location_id, free_time)\
    #    VALUES (1, 1, 100, 1, 23, 27, '00:15')")
    conn.commit()
    conn.close()

    print(load_db())
