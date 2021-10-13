import sys
import time
import os
import config
import ktcon
import setmq
import setdb
import json

queue2 = "robot_main"
prev_devices = ktcon.get_robots()

while True:

    stores = setdb.getStore()
    storeid = ""
    prev_devices = None

    for store in stores:
        storeid = store[1]

    devices = ktcon.get_robots()
    print(devices)

    for device in devices:
        # storeid, ssid, rcode, deviceid, etc, name, status, battery, rtype
        setdb.setDevice(storeid, config.serverid, "KTSR", device["robot_id"],\
            "", "KTSR_" + device["robot_id"], device["status"], device["battery"], 2)
        setmq.send(queue2, {
                    "tp" : "ktstatus",
                    "id" : config.serverid,
                    "ip" : config.ipin,
                    "status" : device["status"],
                    "pstatus" : json.dumps(device),
                    "robotid" : device["robot_id"],
                    "robotip" : "0.0.0.0"
                })

    prev_devices = devices

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(1)      #1초단위로 현재 상태 전달