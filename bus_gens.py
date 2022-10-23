from typing import Iterator
from copy import copy
from cls.Bus import Bus, BusStatus
from cls.User import User, Group
from config import SMALL_BUS_CNT, SMALL_BUS_CAPACITY, BIG_BUS_CNT, BIG_BUS_CAPACITY


u = User(
        id=0,
        login="",
        pwd_hash="",
        salt="",
        group=Group.DRIVER,
        name=""
)


def small_bus_gen():
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
