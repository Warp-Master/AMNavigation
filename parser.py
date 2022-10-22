from collections import defaultdict
from datetime import datetime

import csv
from Flight import Flight
from MyTypes import NameMap, Graph, Edge


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
                id=len(flights),
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
