import config
import requests
import sys
import time
import os

def delivery(table, deviceid, robotid):
    result = 0

    res = requests.get(config.vds_host + "/robot/status", params={"device_id": deviceid, "robot_id": robotid})
    json = res.json()
    # print(json)
    if(json["code"] == 0):
        print(json["data"]["chargeStage"] + " / " + json["data"]["moveState"] + " / " + json["data"]["robotState"])

        if(json["data"]["chargeStage"] == "Idle" and json["data"]["moveState"] == "Idle" and json["data"]["robotState"] == "Free"):
            print("Ready")
            res2 = requests.post(config.vds_host + "/robot/delivery/task", json={
                "deviceId" : deviceid,
                "robotId" : robotid,
                "type" : "new",
                "deliverySort" : "fixed",
                "trays" : [{
                    "destinations" : [{
                    "destination" : table,
                    "id" : "0"
                    }]
                }]
            })
            
            json2 = res2.json()

            print(json2)
            
            if(json2["code"] == 0):
                print("Order set!!")
                res3 = requests.post(config.vds_host + "/robot/action", json={
                    "deviceId" : deviceid,
                    "robotId" : robotid,
                    "action" : "Start"
                })
                json3 = res3.json()
                if(json3["code"] == 0):
                    print("Action ok")
                else:
                    print("Action error")
                    result = 7

            else:
                print("Order error")
                result = 5
        else:
            print("Busy")
            result = 3
    else:
        print("error")
        result = 1

    return result


def status(deviceid, robotid):
    rtnvalue = {
        "status" : "none",
        "battery" : 100,
        "x" : 0,
        "y" : 0,
        "a" : 0
    }

    # print(deviceid + " / " + robotid)
    res = requests.get(config.vds_host + "/robot/status", params={"device_id": deviceid, "robot_id": robotid})
    json = res.json()
    # print(json)
    if(json["code"] == 0):
        print(json["data"]["chargeStage"] + " / " + json["data"]["moveState"] + " / " + json["data"]["robotState"])
        if(json["data"]["chargeStage"] == "Idle" and json["data"]["moveState"] == "Idle" and json["data"]["robotState"] == "Free"):
            print("Ready")
            rtnvalue["status"] = "Ready"
        elif(json["data"]["chargeStage"] != "Idle" and json["data"]["moveState"] == "Idle"):
            print("Charge")
            rtnvalue["status"] = "Charge"
        elif(json["data"]["moveState"] != "Idle"):
            print(json["data"]["moveState"])
            rtnvalue["status"] = json["data"]["moveState"]

        rtnvalue["battery"] = json["data"]["robotPower"]
        rtnvalue["x"] = json["data"]["robotPose"]["x"]
        rtnvalue["y"] = json["data"]["robotPose"]["y"]
        rtnvalue["a"] = json["data"]["robotPose"]["angle"]

    return rtnvalue


# print(delivery("25", "9686649074951", "c0847d1894e6"))