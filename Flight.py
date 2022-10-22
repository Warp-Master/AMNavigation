from dataclasses import dataclass
from datetime import datetime

from MyTypes import Graph, NameMap, Cache
from dijkstra import dijkstra
# used when the start or end points are not found
from constants import DEFAULT_DISTANCE


@dataclass
class Flight:
    id: int
    date: datetime
    flight_type: str
    terminal_name: str
    airline_code: str
    airline_number: int
    airport_code: str
    airport_name: str
    aircraft_type: str
    parking_number: str
    gate_number: str
    passengers_count: int

    def __str__(self):
        return f"{self.airline_code}-{self.airline_number}"

    def get_distance(self, g: Graph, cache: Cache, mapping: NameMap) -> float:
        if self.flight_type == "A":
            start = mapping.get(self.gate_number, None)
            stop = mapping.get(self.parking_number, None)
        elif self.flight_type == "D":
            start = mapping.get(self.parking_number, None)
            stop = mapping.get(self.gate_number, None)
        else:
            raise ValueError(f"bad flight type: {self.flight_type}")

        if start is None or stop is None:
            return DEFAULT_DISTANCE

        distance, parent = dijkstra(g, start, stop, cache)
        return distance[stop]
