var socket = new WebSocket("ws://localhost:8765/ws");
var all_tasks = null;
var tasks_by_id = new Object();
var all_buses = null;
var current_task_id = null;
var selected_bus = "any";
var selected_period = "any";

document.addEventListener("click",function(ev){
    if(ev.target.id.indexOf("tasks-item") != -1){
        if(current_task_id != null){
            var active_item_name = `tasks-item-${current_task_id}`;
            var item = document.getElementById(active_item_name);
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
        var current_task = tasks_by_id[current_task_id];

        document.getElementById("passengers_count").innerText = current_task["passengers_count"];
        document.getElementById("start_time").innerText = current_task["start_time"];
        document.getElementById("end_time").innerText = current_task["end_time"];
        document.getElementById("gate_number").innerText = current_task["gate_number"];
        document.getElementById("parking_number").innerText = current_task["parking_number"];
        document.getElementById("terminal_name").innerText = current_task["terminal_name"];
        document.getElementById("date").innerText = current_task["date"];
        
        var flight_type = "";
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
        var text = "";

        all_tasks.forEach(task => {
            tasks_by_id[task["id"]] = task;

            if(selected_period !== "any"){
                var date = new Date ();
                var now_hours = date.getHours();
                var start_time_segs = task['start_time'].split(":");                
                
                var period_segs = selected_period.split(":");
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
                var ret = true;

                task["buses"].forEach(bus => {
                    if(bus['id'] === Number(selected_bus)){
                        ret = false;
                    }
                });

                if(ret){
                    return;
                }
            }

            var item_name = `tasks-item-${task["id"]}`;
            
            var is_active = "";
            if(current_task_id === task["id"]){
                is_active = "active";
            }
    
            var on_off_line = "";
            if(task["flight_type"] === "A"){
                on_off_line = "Прилетает в:";
            }
            else{
                on_off_line = "Вылетает в:";
            }

            var task_line =`Рейс: ${task["airline_name"]} ${on_off_line} ${task['plan_time']} ${task['date']} Начало задачи: ${task['start_time']} ${task['status']}`;
    
            text += `<li class="list-group-item list-group-item-action ${is_active}" id="${item_name}">${task_line}</li>`;
        });
    
        document.getElementById("tasks_items").innerHTML = text;
    }
}

socket.onmessage = function(event) {    
    var server_data = JSON.parse(event.data);
    all_tasks = server_data["tasks"];
    all_buses = server_data["buses"];

    var is_selected = "";
    if(selected_bus === "any"){
        is_selected = "selected";
    }
    var html_buses = `<option ${is_selected} value="any">Исполнитель (любой)</option>`;

    all_buses.forEach(bus => {
        is_selected = "";
        if(selected_bus === `${bus["id"]}`){
            is_selected = "selected";
        }

        var bus_line = `Автобус № ${bus["id"]} Водитель: ${bus["driver_name"]}`;
        var bus_code = `<option ${is_selected} value="${bus["id"]}">${bus_line}</option>`;
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