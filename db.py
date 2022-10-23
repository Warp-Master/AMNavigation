import asyncio
import sqlite3
import sys
from queue import Queue
from threading import Thread

if __name__ == "__main__":
    conn = sqlite3.connect('bot_db.sqlite')
    cur = conn.cursor()

    cur.execute('CREATE TABLE Task(\
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
        flight_id INTEGER NOT NULL,\
        status TEXT NOT NULL,\
        load_time TEXT NOT NULL,\
        unload_time TEXT NOT NULL\
    )')
    cur.execute('CREATE TABLE Bus(\
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
        current_task_id INTEGER NOT NULL,\
        driver_id INTEGER NOT NULL,\
        capacity INTEGER NOT NULL,\
        status INT NOT NULL,\
        location_id INTEGER NOT NULL,\
        free_location_id INTEGER NOT NULL,\
        free_time TEXT NOT NULL\
    )')
    cur.execute('CREATE TABLE User(\
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
        login TEXT NOT NULL,\
        pwd_hash TEXT NOT NULL,\
        salt TEXT NOT NULL,\
        group_id INTEGER NOT NULL,\
        name TEXT NOT NULL\
    )')
    cur.execute('CREATE TABLE Flight(\
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
        date TEXT NOT NULL,\
        flight_type TEXT NOT NULL,\
        terminal_name TEXT NOT NULL,\
        airline_code TEXT NOT NULL,\
        airline_number INTEGER NOT NULL,\
        airport_code TEXT NOT NULL,\
        airport_name TEXT NOT NULL,\
        aircraft_type TEXT NOT NULL,\
        parking_number TEXT NOT NULL,\
        gate_number TEXT NOT NULL,\
        passengers_count INTEGER NOT NULL\
    )')

    conn.commit()
    cur.close()
    conn.close()
    print('Таблицы успешно созданы!')
    exit()


def get_loop(future: asyncio.Future) -> asyncio.AbstractEventLoop:
    if sys.version_info >= (3, 7):
        return future.get_loop()
    else:
        return future._loop


class DBWorker(Thread):
    def __init__(self):
        super().__init__()
        self.tasks = Queue()

    def run(self) -> None:
        self.adb = sqlite3.connect('bot_db.sqlite')

        def set_result(fut, result):
            if not fut.done():
                fut.set_result(result)
        while True:
            type_task, sql, commit_all, future = self.tasks.get()
            # print(sql)
            try:
                if type_task == 1:
                    self.adb.execute(sql)
                    if commit_all:
                        self.adb.commit()
                    if future is not None:
                        get_loop(future).call_soon_threadsafe(set_result, future, None)
                elif type_task == 2:
                    cur = self.adb.execute(sql)
                    if commit_all:
                        res = cur.fetchall()
                    else:
                        res = cur.fetchone()
                    get_loop(future).call_soon_threadsafe(set_result, future, res)
                elif type_task == 3:
                    self.adb.commit()

            except Exception as ex:
                print('db error', ex)

    async def execute_wait(self, sql, commit=True):
        future = asyncio.get_event_loop().create_future()
        task = (1, sql, commit, future,)
        self.tasks.put_nowait(task)
        await future

    def execute(self, sql, commit=True):
        task = (1, sql, commit, None)
        self.tasks.put_nowait(task)

    def commit(self):
        task = (3, None, None, None)
        self.tasks.put_nowait(task)

    async def execute_with_res(self, sql, fetchall=True):
        future = asyncio.get_event_loop().create_future()

        task = (2, sql, fetchall, future,)
        self.tasks.put_nowait(task)

        return await future


database = DBWorker()
database.start()


def execute_with_res_o(sql, fetchall=True):
    database = sqlite3.connect('bot_db.sqlite')
    cur = database.execute(sql)
    if fetchall:
        res = cur.fetchall()
    else:
        res = cur.fetchone()
    database.close()
    return res
