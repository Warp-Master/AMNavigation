import asyncio
import sqlite3
from queue import Queue
from threading import Thread
from enum import Enum

if __name__ == "__main__":
    # Первоначальная инциализация бд из csv файлов
    conn = sqlite3.connect('bot_db.sqlite')
    cur = conn.cursor()

    cur.execute('CREATE TABLE Task(\
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
        flight_id INTEGER NOT NULL,\
        status TEXT NOT NULL,\
        start_time TEXT NOT NULL,\
        finish_time TEXT NOT NULL\
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
    cur.execute('CREATE TABLE Users(\
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


class TaskType(Enum):
    """Тип задачи"""
    WITHOUT_RES = 0
    WITH_RES = 1
    COMMIT = 2


class DBWorker(Thread):
    """Тред отвечающий за работу за бд"""
    def __init__(self):
        super().__init__()
        self.tasks = Queue()
        self.adb = None

    def run(self) -> None:
        self.adb = sqlite3.connect('bot_db.sqlite')

        def set_result(fut, result):
            if not fut.done():
                fut.set_result(result)
        while True:
            task_type, sql, commit_all, future = self.tasks.get()
            # print(sql)
            try:
                if task_type == TaskType.WITHOUT_RES:
                    self.adb.execute(sql)
                    if commit_all:
                        self.adb.commit()
                    if future is not None:
                        future.get_loop().call_soon_threadsafe(set_result, future, None)
                elif task_type == TaskType.WITH_RES:
                    cur = self.adb.execute(sql)
                    if commit_all:
                        res = cur.fetchall()
                    else:
                        res = cur.fetchone()
                    future.get_loop().call_soon_threadsafe(set_result, future, res)
                elif task_type == TaskType.COMMIT:
                    self.adb.commit()

            except Exception as ex:
                print('db error', ex)

    async def execute_wait(self, sql, commit=True):
        """Корутина исполнения sql запроса в бд"""
        future = asyncio.get_event_loop().create_future()
        task = (TaskType.WITHOUT_RES, sql, commit, future)
        self.tasks.put_nowait(task)
        await future

    def execute(self, sql, commit=True):
        """Добавление задачи в очередь"""
        task = (TaskType.WITHOUT_RES, sql, commit, None)
        self.tasks.put_nowait(task)

    def commit(self):
        """Отправление данных в бд"""
        task = (TaskType.COMMIT, None, None, None)
        self.tasks.put_nowait(task)

    async def execute_with_res(self, sql, fetchall=True):
        """Корутина исполнения sql запроса в бд с возвращением результата"""
        future = asyncio.get_event_loop().create_future()

        task = (TaskType.WITH_RES, sql, fetchall, future)
        self.tasks.put_nowait(task)

        return await future


database = DBWorker()
database.start()


# def execute_with_res_o(sql, fetchall=True):
#     """Выполняет с возвращением результата"""
#     database = sqlite3.connect('bot_db.sqlite')
#     cur = database.execute(sql)
#     if fetchall:
#         res = cur.fetchall()
#     else:
#         res = cur.fetchone()
#     database.close()
#     return res
