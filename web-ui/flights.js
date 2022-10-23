let socket = new WebSocket("ws://localhost:8765/ws");
let all_tasks = null;
let tasks_by_id = {};
let all_buses = null;
let current_task_id = null;
let selected_bus = "any";
let selected_period = "any";

document.addEventListener("click",function(ev){
    if(ev.target.id.indexOf("tasks-item") !== -1){
        if(current_task_id != null){
            let active_item_name = `tasks-item-${current_task_id}`;
            let item = document.getElementById(active_item_name);
            if(item != null){
                item.classList.remove('active');
            }            
        }
        
        ev.target.classList.add('active');
        current_task_id = Number(ev.target.id.split("-")[2]);

        document.getElementById("task-info-cont").hidden = false;
        
        rewrite_current_task();
    }
});

function get_bus_line(bus){
    return `Автобус № ${bus["id"]} Водитель: ${bus["driver_name"]}`;
}

function rewrite_current_task(){
    if(current_task_id != null){
        var delayed_start_time = document.getElementById("delayed_start_time_id");
        var delayed_end_time = document.getElementById("delayed_end_time_id");
        delayed_start_time.value = "";
        delayed_end_time.value = "";

        const current_task = tasks_by_id[current_task_id];

        document.getElementById("passengers_count").innerText = current_task["passengers_count"];
        document.getElementById("start_time").innerText = current_task["start_time"];
        document.getElementById("end_time").innerText = current_task["end_time"];
        document.getElementById("gate_number").innerText = current_task["gate_number"];
        document.getElementById("parking_number").innerText = current_task["parking_number"];
        document.getElementById("terminal_name").innerText = current_task["terminal_name"];
        document.getElementById("date").innerText = current_task["date"];
        
        let flight_type = "";
        if(flight_type === "A"){
            flight_type = "На выход";
        }
        else{
            flight_type = "На самолёт";
        }

        document.getElementById("flight_type").innerText = flight_type;
        document.getElementById("airline_name").innerText = current_task["airline_name"];
        document.getElementById("plan_time").innerText = current_task["plan_time"];
        document.getElementById("aircraft_type").innerText = current_task["aircraft_type"];

        let allowed_bus_100 = [];
        let allowed_bus_50 = [];

        all_buses.forEach(bus => {
            let is_add = true;

            current_task["buses"].forEach(task_bus => {
                if(task_bus["id"] === bus["id"]){
                    is_add = false;
                }
            });

            if(is_add){
                if(bus['type'] === 100){
                    allowed_bus_100.push(bus);
                }
                else{
                    allowed_bus_50.push(bus);
                }
            }

        });

        let html_buf_100 = "";
        let html_buf_50 = "";

        current_task["buses"].forEach(bus => {
            let html_bus_select = "";
            let allowed_buses;

            if(bus['type'] === 100){
                allowed_buses = allowed_bus_100;
            }
            else{
                allowed_buses = allowed_bus_50;
            }

            let bus_line = get_bus_line(bus);
            let html_bus_item = `<option selected value="${bus['id']}">${bus_line}</option>`;
            html_bus_select += html_bus_item;

            allowed_buses.forEach(allowed_bus => {
                bus_line = get_bus_line(allowed_bus);
                html_bus_item = `<option value="${allowed_bus['id']}">${bus_line}</option>`;
                html_bus_select += html_bus_item;
            });

            let html_bus = `<br><select class="form-select" id="select-bus-item-${bus['id']}" onchange="select_bus(${bus['id']})">${html_bus_select}</select>`;

            if(bus['type'] === 100){
                html_buf_100 += html_bus;
            }
            else{
                html_buf_50 += html_bus;
            }
        });

        document.getElementById("buses_100").innerHTML = html_buf_100;
        document.getElementById("buses_50").innerHTML = html_buf_50;
    }
}

function rewrite_tasks(){
    if(all_tasks != null){
        let text = "";

        all_tasks.forEach(task => {
            tasks_by_id[task["id"]] = task;

            if(selected_period !== "any"){
                let date = new Date ();
                let now_hours = date.getHours();
                let start_time_segs = task['start_time'].split(":");                
                
                let period_segs = selected_period.split(":");
                if(period_segs[0] === "p"){
                    if(Number(start_time_segs[0]) > now_hours || now_hours - Number(period_segs[1]) > Number(start_time_segs[0])){
                        //TODO return by status
                        return;
                    }
                }
                else{
                    if(Number(start_time_segs[0]) < now_hours || now_hours + Number(period_segs[1]) < Number(start_time_segs[0])){
                        //TODO return by status
                        return;
                    }
                }
            }

            if(selected_bus !== "any"){
                let ret = true;

                //TODO get by id
                task["buses"].forEach(bus => {
                    if(bus['id'] === Number(selected_bus)){
                        ret = false;
                    }
                });

                if(ret){
                    return;
                }
            }

            let item_name = `tasks-item-${task["id"]}`;
            
            let is_active = "";
            if(current_task_id === task["id"]){
                is_active = "active";
            }
    
            let on_off_line = "";
            if(task["flight_type"] === "A"){
                on_off_line = "Прилетает в:";
            }
            else{
                on_off_line = "Вылетает в:";
            }

            let task_line =`Рейс: ${task["airline_name"]}<br>${on_off_line} ${task['plan_time']} ${task['date']}<br>Начало задачи: ${task['start_time']}<br>${task['status']}`;
    
            text += `<li class="list-group-item list-group-item-action ${is_active}" id="${item_name}">${task_line}</li>`;
        });
    
        document.getElementById("tasks_items").innerHTML = text;
    }
}

socket.onmessage = function(event) {    
    let server_data = JSON.parse(event.data);
    all_tasks = server_data["tasks"];
    all_buses = server_data["buses"];

    let is_selected = "";
    if(selected_bus === "any"){
        is_selected = "selected";
    }
    let html_buses = `<option ${is_selected} value="any">Исполнитель (любой)</option>`;

    all_buses.forEach(bus => {
        is_selected = "";
        if(selected_bus === `${bus["id"]}`){
            is_selected = "selected";
        }

        let bus_line = get_bus_line(bus);
        let bus_code = `<option ${is_selected} value="${bus["id"]}">${bus_line}</option>`;
        html_buses += bus_code;
    })
    document.getElementById("select_driver").innerHTML = html_buses;

    rewrite_tasks();
    rewrite_current_task();
};

function select_driver(){
    selected_bus = document.getElementById("select_driver").value;
    rewrite_tasks();
}

function select_period(){
    selected_period = document.getElementById("select_period").value;
    rewrite_tasks();
}

function select_bus(id_bus){
    var bus_item = document.getElementById(`select-bus-item-${id_bus}`);
    var selected_bus = bus_item.value;
    const current_task = tasks_by_id[current_task_id];

    current_task['buses'].forEach(bus_s => {
        if(bus_s['id'] === id_bus){
            bus_s['rewrite_to'] = selected_bus;
        }
    });
}

function save_changes(){
    const current_task = tasks_by_id[current_task_id];
    var delayed_start_time = document.getElementById("delayed_start_time_id");
    var delayed_end_time = document.getElementById("delayed_end_time_id");

    update = {
        'task_id':current_task_id,
        'delayed_start_time':Number(delayed_start_time.value),
        'delayed_end_time':Number(delayed_end_time.value),
        'buses':current_task['buses']
    };

    socket.send(JSON.stringify(update));
    alert("Сохранено!");
}