import sys
import time
import os
import config
import vdcon
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
        if(device[10] == 2 and device[1] == "VDCS"):
            # print(device)
            rstatus = vdcon.status(device[4], device[3])
            print(rstatus)
            if(rstatus != ""):
                #               storeid, ssid,          rcode,      deviceid, etc, name, status, battery, rtype
                setdb.setDevice(storeid, config.serverid, "VDCS", device[3], device[2], device[5], rstatus["status"], rstatus["battery"], 2)

                setmq.send(queue2, {
                    "tp" : "vdstatus",
                    "id" : config.serverid,
                    "ip" : config.ipin,
                    "status" : rstatus["status"],
                    "pstatus" : str(rstatus),
                    "robotid" : device[3],
                    "robotip" : "0.0.0.0"
                })

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep')
    time.sleep(3)      #1초단위로 현재 상태 전달