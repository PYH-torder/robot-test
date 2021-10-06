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
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuYXBpIn0.kaUFD989K_jzH5FITAqy6uq3035KB23kh27pq2stpuk"
AUTH_TOKEN_PREFIX = "Bearer "
HTTP_HEADERS = {
    "Accept": "application/json",
    "Authorization": AUTH_TOKEN_PREFIX + AUTH_TOKEN
}
SITE_ID = "656fa13493fc4aafa3c9cdfe3eec8df7"

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
    print("==== ktcon http error ====")
    print("Response data :", res_json)
    
    try :
        print("Timestamp :", res_json["timestamp"])
    except :
        print("Timestamp :", datetime.datetime.now())
    
    try :
        print("HTTP status :", res_json["status"], res_json["error"])
    except :
        print("HTTP status :", res_json["code"])
    
    try :
        print("Error message :", res_json["message"])
    except :
        print("Error message :", res_json["msg"])

    print("==========================", flush = True)

def get_robots() :
    url = get_default_api_url() + "/status/" + SITE_ID + "/robots"
    res = api_request("get", url)
    robots = []
    for robot in res["list"]:
        robots.append(robot)
    return robots

def get_robot_status(robot_id) : 
    url = get_default_api_url() + "/status/" + SITE_ID + "/robots/" + robot_id
    res = api_request("get", url)
    return res["data"]

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
#pprint(get_robot_status('1234567890'))
pprint(get_nodes())
#pprint(get_node_by_id("NO-40311075"))
#pprint(start_mission("1234567890", "moving", "NO-80529038", "test_item"))
#pprint(stop_mission('1234567890211006165748147'))