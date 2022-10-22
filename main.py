from collections import namedtuple, defaultdict
import csv
from datetime import datetime
from dataclasses import dataclass


Edge = namedtuple("Edge", ("id", "to", "distance"))
Vertex = namedtuple("Vertex", ("id", ))


@dataclass
class Flight:
    date: datetime
    flight_type: str
    terminal_name: str
    airline_code: str
    airline_number: int
    airport_code: str
    airport_name: str
    aircraft_type: str
    parking_place: str
    gate_number: str
    passengers_count: int

    def __str__(self):
        return f"{self.airline_code}-{self.airline_number}"


def main():
    name_mapping = dict()
    graph = defaultdict(list)

    # create name mapping
    with open("name-map.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)  # skip header
        for row in reader:
            name_mapping[row[1]] = row[0]

    # build graph
    with open("edges.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)  # skip header
        for row in reader:  # make undirected graph
            a = Vertex(row[1])
            b = Vertex(row[2])
            graph[a.id].append(Edge(int(row[0]), b.id, int(row[3])))
            graph[b.id].append(Edge(int(row[0]), a.id, int(row[3])))

    with open("timetable.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)  # skip header
        for row in reader:
            flight = Flight(
                date=datetime.strptime(f"{row[0]} {row[5]}", "%d.%m.%Y %H:%M"),
                flight_type=row[1],
                terminal_name=row[2],
                airline_code=row[3],
                airline_number=int(row[4]),
                airport_code=row[6],
                airport_name=row[7],
                aircraft_type=row[8],
                parking_place=row[9],
                gate_number=row[10],
                passengers_count=int(row[11]),
            )
            print(flight)

    # testing section
    # print(name_mapping)
    # print(*graph.items(), sep="\n")


if __name__ == "__main__":
    main()
