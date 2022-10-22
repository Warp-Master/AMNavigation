from collections import defaultdict
from datetime import datetime
import sqlite3
import csv

conn = sqlite3.connect('bot_db.sqlite')
cur = conn.cursor()

with open("csv/timetable.csv",encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader, None)  # skip header
    for row in reader:
        cur.execute('INSERT INTO Flight\
            (date, flight_type, terminal_name, airline_code,\
            airline_number, airport_code, airport_name, aircraft_type,\
            parking_number, gate_number, passengers_count)\
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\
                ', (datetime.strptime(f"{row[0]} {row[5]}", "%d.%m.%Y %H:%M"), row[1], row[2], 
                row[3], int(row[4]), row[6], row[7], row[8], row[9], row[10], int(row[11])))

#for test
cur.execute('SELECT * FROM Flight')
for row in cur.fetchall():
    print(row)