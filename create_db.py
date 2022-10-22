import sqlite3

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
    status TEXT NOT NULL,\
    location_id INTEGER NOT NULL\
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
conn.close()

print('Таблицы успешно созданы!')