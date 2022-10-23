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

function rewrite_current_task(){
    if(current_task_id != null){
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

        let bus_line = `Автобус № ${bus["id"]} Водитель: ${bus["driver_name"]}`;
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