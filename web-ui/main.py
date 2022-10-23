import asyncio, json
import websockets

#тестовая заглушка для взаимодействия с web-ui

async def echo(websocket):
    task = {
        'id':56,
        'flight_type':'A',
        'date':'23.02.2003',
        'airline_name':'SU2563',
        'aircraft_type':'asf45',
        'start_time':'5:00',
        'end_time':'02:05',
        'plan_time':'06:56',
        'terminal_name':'D',
        'gate_number':'DGA_D',
        'parking_number':'42',
        'status':'Едет',
        'passengers_count':645,
        'buses': [
            {
                'id':5,
                'driver_id':2,
                'driver_name':'Петров',
                'type':100,
                'status':'Все норм'
            },
            {
                'id':2,
                'driver_id':5,
                'driver_name':'Сидоров',
                'type':50,
                'status':'Все норм'
            }
        ]
    }

    buses = [
        {
            'id':5,
            'driver_name':'Петров',
            'type':100
        },
        {
            'id':2,
            'driver_name':'Сидоров',
            'type':50
        },
        {
            'id':3,
            'driver_name':'Иванов',
            'type':100
        },
        {
            'id':4,
            'driver_name':'Михайлов',
            'type':50
        }
    ]

    task2 = task.copy()
    task2['id'] = 10
    task2['airline_name'] = 'M546'
    task2['flight_type'] = 'D'
    task2['start_time'] = '4:00'

    task3 = task.copy()
    task3['id'] = 11
    task3['airline_name'] = 'TU856'
    task3['start_time'] = '2:00'

    task4 = task.copy()
    task4['flight_type'] = 'D'
    task4['id'] = 12
    task4['airline_name'] = 'MGR455'
    task4['start_time'] = '1:00'

    task5 = task.copy()
    task5['flight_type'] = 'D'
    task5['id'] = 13
    task5['airline_name'] = 'SU668'
    task5['start_time'] = '6:00'

    task6 = task.copy()
    task6['flight_type'] = 'D'
    task6['id'] = 4
    task6['airline_name'] = 'TU566'
    task6['start_time'] = '7:00'
    task6['buses'] = [
        {
            'id':5,
            'driver_id':2,
            'driver_name':'Петров',
            'type':100,
            'status':'Все норм'
        },
        {
            'id':3,
            'driver_id':6,
            'driver_name':'Иванов',
            'type':50,
            'status':'Все норм'
        }
    ]
    tasks = {
        'tasks':[task,task2,task3,task4,task5,task6],
        'buses':buses
    }     

    task_by_ids = dict()
    for ts in tasks['tasks']:
        task_by_ids[ts['id']] = ts

    buses_by_ids = dict()
    for ts in tasks['buses']:
        buses_by_ids[ts['id']] = ts

    await websocket.send(json.dumps(tasks))

    while True:
        async for message in websocket:
            data = json.loads(message)
            print(message)
        #await asyncio.get_event_loop().run_in_executor(None,input,"Write mode:")
    """
    text = dict()
    while True:
        cmd = await asyncio.get_event_loop().run_in_executor(None,input,"Write mode:")
        txt = text.setdefault(cmd,"")
        txt += await asyncio.get_event_loop().run_in_executor(None,input,"Write text:") +'\n'
        text[cmd] = txt
        await websocket.send(cmd+"|||"+txt)
    """

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())