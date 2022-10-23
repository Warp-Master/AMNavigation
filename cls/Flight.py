from dataclasses import dataclass
from datetime import datetime
from db import DBWorker

from MyTypes import Graph, NameMap, Cache
from dijkstra import dijkstra
# used when the start or end points are not found
from config import DEFAULT_DISTANCE


@dataclass
class Flight:
    """Датакласс с данными рейса"""
    def __init__(self, flight_id: int, date: datetime, flight_type: str, terminal_name: str, airline_code: str,
                 airline_number: int, airport_code: str, airport_name: str, aircraft_type: str, parking_number: str,
                 gate_number: str, passengers_count: int) -> None:
        self.id: int = flight_id
        self.date: datetime = date
        self.type: str = flight_type
        self.terminal_name: str = terminal_name
        self.airline_code: str = airline_code
        self.airline_number: int = airline_number
        self.airport_code: str = airport_code
        self.airport_name: str = airport_name
        self.aircraft_type: str = aircraft_type
        self.parking_number: str = parking_number
        self.gate_number: str = gate_number
        self.passengers_count: int = passengers_count

    def __str__(self):
        return f"{self.airline_code}-{self.airline_number}"

    def __lt__(self, other: "Flight") -> bool:
        return self.date < other.date

    def __gt__(self, other: "Flight") -> bool:
        return self.date > other.date

    def update(self, db: DBWorker):
        """Обновление в бд"""
        db.execute(f"UPDATE Flight SET date = '{self.date.strftime('%d.%m.%Y %H:%M')}',\
            flight_type = '{self.type}', \
            terminal_name = '{self.terminal_name}',\
            airline_code = '{self.airline_code}',\
            airline_number = '{self.airline_number}',\
            airport_code = '{self.airport_code}',\
            airport_name = '{self.airport_name}',\
            aircraft_type = '{self.aircraft_type}',\
            parking_number = '{self.parking_number}',\
            gate_number = '{self.gate_number}',\
            passengers_count = '{self.passengers_count}'\
            WHERE id = '{self.id}'")

    def get_distance(self, g: Graph, cache: Cache, mapping: NameMap) -> float:
        """Возвращает расстояние между терминалом и самолётом в метрах в зависимости от типа рейса"""
        if self.type == "A":
            start = mapping.get(self.gate_number, None)
            stop = mapping.get(self.parking_number, None)
        elif self.type == "D":
            start = mapping.get(self.parking_number, None)
            stop = mapping.get(self.gate_number, None)
        else:
            raise ValueError(f"bad flight type: {self.type}")

        if start is None or stop is None:
            return DEFAULT_DISTANCE

        return dijkstra(g, start, stop, cache)[stop]
