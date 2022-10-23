from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from enum import Enum
from operator import methodcaller, itemgetter

from MyTypes import Graph, Cache, TaskSolution
from cls.Task import Task
from cls.User import User
from config import SPEED_LIMIT
from db import DBWorker
from dijkstra import dijkstra


class BusStatus(Enum):
    WAITING = 0
    MOVING = 1
    LOADING = 2
    UNLOADING = 3


@dataclass
class Bus:
    """Дата класс с данными автобуса"""
    id: int
    task: Task | None
    driver: User
    capacity: int
    status: BusStatus
    location_id: int | None
    free_location_id: int | None
    free_time: datetime | None

    def time_for_delivery(self, start_time: datetime, graph: Graph, cache: Cache, target_id: int) -> timedelta:
        """Возвращает время необходимое, чтобы автобус доехал до target_id, начав в start_time"""
        if self.status == BusStatus.WAITING:
            distance = dijkstra(graph, self.location_id, target_id, cache)[target_id]
            return timedelta(seconds=distance / SPEED_LIMIT)
        else:
            distance = dijkstra(graph, self.free_location_id, target_id, cache)[target_id]
            return max(timedelta(), self.free_time - start_time) + timedelta(seconds=distance / SPEED_LIMIT)

    def update(self, db: DBWorker):
        """Обновляет запись в бд"""
        db.execute(f"UPDATE Bus SET current_task_id = '{self.task.id}',\
            driver_id = '{self.driver.id}', \
            capacity = '{self.capacity}',\
            status = '{self.status}',\
            location_id = '{self.location_id}',\
            free_location_id = '{self.free_location_id}',\
            free_time = '{self.free_time.strftime('%H:%M')}',\
            WHERE id = '{self.id}'")


class BusPool:
    """Оптимизационный пул автобусов"""
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
        for big_cnt in range(pass_cnt // 100 + (pass_cnt % 100 > 0) + 1):
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
