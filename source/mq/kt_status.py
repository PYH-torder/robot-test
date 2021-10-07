import sys
import time
import os
import config
import ktcon
import setmq
import setdb

queue2 = "robot_main"

while True:

    stores = setdb.getStore()
    storeid = ""

    for store in stores:
        storeid = store[1]

    devices = ktcon.get_robots()

    for device in devices:
        if(device["status"] != "Unknown status"):
            # storeid, ssid, rcode, deviceid, etc, name, status, battery, rtype
            setdb.setDevice(storeid, config.serverid, "KTSR", device["robot_id"],\
                "", "KTSR_" + device["robot_id"], device["status"], device["battery"], 2)

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(3)      #3초단위로 현재 상태 전달