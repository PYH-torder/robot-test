import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
import config
from robot_controller import lgs_con
from mq_util import mq_util
from dao import store_dao
from dao import device_dao

queue2 = "robot_main"

# rtn = lgscon.devicelist()
# print(rtn)

while True:

    stores = store_dao.find_store()
    storeid = ""

    for store in stores:
        # print(store[1])
        storeid = store[1]

    devices = device_dao.find_device()

    for device in devices:
        # print(device[10], device[1])
        if(device[10] == 2 and device[1] == "LGSR"):
            print("LGSR check", device[3])
            rstatus = lgs_con.status(device[3])
            print(rstatus)
            if(rstatus != ""):
                device_dao.save_device(storeid, config.server_id, "LGSR", device[3], device[2], device[5], rstatus["status"], rstatus["battery"], 2)

                mq_util.send(queue2, {
                    "tp" : "lgstatus",
                    "id" : config.server_id,
                    "ip" : config.ipin,
                    "status" : rstatus["status"],
                    "pstatus" : str(rstatus),
                    "robotid" : device[3],
                    "robotip" : "0.0.0.0"
                })

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(3)      #1초단위로 현재 상태 전달