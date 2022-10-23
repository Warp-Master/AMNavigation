from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from enum import Enum

from MyTypes import Graph, Cache
from Task import Task
from User import User
from config import SPEED_LIMIT
from dijkstra import dijkstra


class BusStatus(Enum):
    WAITING = 0
    MOVING = 1
    LOADING = 2
    UNLOADING = 3


@dataclass
class Bus:
    id: int
    task: Task | None
    driver: User
    capacity: int
    status: BusStatus
    location_id: int | None
    free_location_id: int | None
    free_time: datetime | None



    def time_for_delivery(self, start_time: datetime, graph: Graph, cache: Cache, target_id: int) -> timedelta:
        if self.status == BusStatus.WAITING:
            distance = dijkstra(graph, self.location_id, target_id, cache)[target_id]
            return timedelta(seconds=distance / SPEED_LIMIT)
        else:
            distance = dijkstra(graph, self.free_location_id, target_id, cache)[target_id]
            return max(timedelta(), self.free_time - start_time) + timedelta(seconds=distance / SPEED_LIMIT)
