import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import sys
import time
import os
import config
from robot_controller import vd_con
from mq_util import mq_util
from dao import store_dao
from dao import device_dao

while True:

    stores = store_dao.find_store()
    storeid = ""

    for store in stores:
        print(store[1])
        storeid = store[1]

    devices = device_dao.find_device()
    for device in devices:
        if(device[10] == 2 and device[1] == "VDCS"):
            # print(device)
            rstatus = vd_con.status(device[4], device[3])
            print(rstatus)
            if(rstatus != ""):
                #               storeid, ssid,          rcode,      deviceid, etc, name, status, battery, rtype
                device_dao.save_device(storeid, config.server_id, "VDCS", device[3], device[2], device[5], rstatus["status"], rstatus["battery"], 2)

                mq_util.send(config.mqnm, {
                    "tp" : "vdstatus",
                    "id" : config.server_id,
                    "ip" : config.ipin,
                    "status" : rstatus["status"],
                    "pstatus" : str(rstatus),
                    "robotid" : device[3],
                    "robotip" : "0.0.0.0"
                })

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(3)      #1초단위로 현재 상태 전달