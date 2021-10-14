import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
import config
from robot_controller import dyc_con
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
        if(device[10] == 3 and device[1] == "DYCM"):
            # print(device)
            rstatus = dyc_con.status()
            print(rstatus)
            if(rstatus != ""):
                # storeid, ssid, rcode, deviceid, etc, name, status, battery, rtype
                device_dao.save_device(storeid, config.server_id, "DYCM", device[3], device[2], device[5], rstatus, 100, 3)

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(3)      #1초단위로 현재 상태 전달