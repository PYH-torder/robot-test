import config
import requests
import sys
import time
import os
import json
import datetime
from pprint import pprint

HOST = "211.184.190.64:40080"
API_DEFAULT_PATH = "/rmapis"
AUTH_TOKEN_PREFIX = "Bearer "
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuYXBpIn0.kaUFD989K_jzH5FITAqy6uq3035KB23kh27pq2stpuk"
HTTP_HEADERS = {
    "Accept": "application/json",
    "Authorization": AUTH_TOKEN_PREFIX + AUTH_TOKEN
}
SITE_ID = "7ff8541b5dee4e1bb3b1c802723caa56"

def get_default_api_url() :
    return "http://" + HOST + API_DEFAULT_PATH

def api_request(method, url, data = {}) :
    res = None
    try :
        res = getattr(requests, method)(url, headers = HTTP_HEADERS, data = json.dumps(data)).json()
        if res["success"] :
            return res
        else :
            raise Exception()
    except :
        http_error_handler(res)
        return None

def http_error_handler(res_json) :
    print("==== ktcon http error ====", file = sys.stderr)
    print("Response data :", res_json, file = sys.stderr)
    
    try :
        print("Timestamp :", res_json["timestamp"], file = sys.stderr)
    except :
        print("Timestamp :", datetime.datetime.now(), file = sys.stderr)
    
    try :
        print("HTTP status :", res_json["status"], res_json["error"], file = sys.stderr)
    except :
        print("HTTP status :", res_json["code"], file = sys.stderr)
    
    try :
        print("Error message :", res_json["message"], file = sys.stderr)
    except :
        print("Error message :", res_json["msg"], file = sys.stderr)

    print("==========================", flush = True, file = sys.stderr)

def get_robots() :
    url = get_default_api_url() + "/status/" + SITE_ID + "/robots"
    res = api_request("get", url)
    robots = []
    for robot in res["list"]:
        robots.append(convert_robot_status(robot))
    return robots

def get_robot_status(robot_id) : 
    url = get_default_api_url() + "/status/" + SITE_ID + "/robots/" + robot_id
    res = api_request("get", url)
    
    return convert_robot_status(res["data"])

def convert_robot_status(robot_obj) :
    res_obj = {
        "battery": robot_obj["battery"],
        "create_time": robot_obj["createTime"],
        "heading": robot_obj["heading"],
        "robot_id": robot_obj["robotId"],
        "x": robot_obj["x"],
        "y": robot_obj["y"]
    }
    print(robot_obj["robotId"], robot_obj["driveStatus"])
    if robot_obj["driveStatus"] == 0 :
        res_obj["status"] = "Ready"
    elif robot_obj["driveStatus"] == 1 or robot_obj["driveStatus"] == 2 or \
        robot_obj["driveStatus"] == 3 or robot_obj["driveStatus"] == 4 :
        res_obj["status"] = "Moving"
    elif robot_obj["driveStatus"] == 5 or robot_obj["driveStatus"] == 6 or \
        robot_obj["driveStatus"] == 7 or robot_obj["driveStatus"] == 8 or \
        robot_obj["driveStatus"] == 12 :
        print("ktcon drive status detail - robot id :",robot_obj["robot_id"],\
            ", code :", robot_obj["driveStatus"])
        res_obj["status"] = "Stop"
    elif robot_obj["driveStatus"] == 9 :
        res_obj["status"] = "Manual mode"
    elif robot_obj["driveStatus"] == 10 or robot_obj["driveStatus"] == 11 : 
        res_obj["status"] = "Onboard elevator"
    else :
        res_obj["status"] = "Unknown status"

    return res_obj

def get_ready_robot() :
    robots = get_robots()
    for robot in robots :
        if robot["driveStatus"] == 0 :
            return robot
    return None

def get_nodes() :
    url = get_default_api_url() + "/map/" + SITE_ID + "/nodes"
    res = api_request("get", url)
    return res["list"]

def get_node_by_id(node_id = "") :
    url = get_default_api_url() + "/map/" + SITE_ID + "/nodes/" + node_id
    res = api_request("get", url)
    return res["data"]

class Task :
    def __init__(self, task_code, seq, repeat) :
        self.task_code = task_code
        self.seq = seq
        self.task_data = {
            "goal": [],
            "itemList": []
        }
        self.repeat = repeat
    
    def add_task_data(self, goal, item) :
        self.task_data["goal"].append(goal)
        self.task_data["itemList"].append(item)
    
    def to_plain_object(self) :
        return {
            "taskCode": self.task_code,
            "seq": self.seq,
            "taskData": self.task_data
        }

class Mission :
    def __init__(self, robot_id, mission_code) :
        self.robot_id = robot_id
        self.mission_code = mission_code
        self.tasks = []
    
    def add_task(self, task) :
        self.tasks.append(task)

    def to_plain_object(self) :
        res = {
            "robotId": self.robot_id,
            "missionCode": self.mission_code,
            "task": []
        }
        for task in self.tasks :
            res["task"].append(task.to_plain_object())
        return res

def start_mission(robot_id, task_type, goal, item) :
    url = get_default_api_url() + "/mission/mission"
    mission = Mission(robot_id, "test_mission_code")
    dummy_task = Task(task_type, 1, 1)
    dummy_task.add_task_data(goal, item)
    mission.add_task(dummy_task)
    
    res = api_request("post", url, mission.to_plain_object())
    return res["data"]

def stop_mission(mission_id) :
    url = get_default_api_url() + "/mission/control/mscancel/" + mission_id
    res = api_request("post", url)
    return res["data"]

#pprint(json.dumps({}))
#pprint(get_robots())
#pprint(get_robot_status('1234567890'))
#pprint(get_nodes())
#pprint(get_node_by_id("NO-40311075"))
#pprint(start_mission("1234567890", "moving", "NO-80529038", "test_item"))
#pprint(stop_mission('1234567890211006165748147'))