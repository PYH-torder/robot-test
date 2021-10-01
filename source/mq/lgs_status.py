import sys
import time
import os
import config
import lgscon
import setmq
import setdb

queue2 = "robot_main"

# rtn = lgscon.devicelist()
# print(rtn)

while True:

    stores = setdb.getStore()
    storeid = ""

    for store in stores:
        # print(store[1])
        storeid = store[1]

    devices = setdb.getDevice()

    for device in devices:
        # print(device[10], device[1])
        if(device[10] == 2 and device[1] == "LGSR"):
            print("LGSR check", device[3])
            rstatus = lgscon.status(device[3])
            print(rstatus)
            if(rstatus != ""):
                setdb.setDevice(storeid, config.serverid, "LGSR", device[3], device[2], device[5], rstatus["status"], rstatus["battery"], 2)

                setmq.send(queue2, {
                    "tp" : "lgstatus",
                    "id" : config.serverid,
                    "ip" : config.ipin,
                    "status" : rstatus["status"],
                    "pstatus" : str(rstatus),
                    "robotid" : device[3],
                    "robotip" : "0.0.0.0"
                })

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(3)      #1초단위로 현재 상태 전달