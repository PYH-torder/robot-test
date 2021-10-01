import sys
import time
import os
import config
import dyccon
import setmq
import setdb

queue2 = "robot_main"

while True:

    stores = setdb.getStore()
    storeid = ""

    for store in stores:
        print(store[1])
        storeid = store[1]

    devices = setdb.getDevice()

    for device in devices:
        if(device[10] == 3 and device[1] == "DYCM"):
            # print(device)
            rstatus = dyccon.status()
            print(rstatus)
            if(rstatus != ""):
                # storeid, ssid, rcode, deviceid, etc, name, status, battery, rtype
                setdb.setDevice(storeid, config.serverid, "DYCM", device[3], device[2], device[5], rstatus, 100, 3)

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep')
    time.sleep(3)      #1초단위로 현재 상태 전달