import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from indy_utils import indydcp_client as client
import sys
import time
import os
import config
from mq_util import mq_util
from dao import store_dao
from dao import device_dao

robot_ip = config.nmr_ip  # Robot (Indy) IP
robot_name = config.nmr_name  # Robot name (Indy7)

indy_status = None
indy_program_state = None
indy_connected_status = None
indy_send_status = "Fix"

while True:
    try:
        indy = client.IndyDCPClient(robot_ip, robot_name)
        indy_connected_status = False

        try: 
            indy.connect()
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '!!fail indy connect')
            indy.disconnect()
        else:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), 'success indy connect')
            indy_connected_status = True

        val1 = 0
        val2 = 0
        
        if(indy_connected_status):
            try:
                indy_status = indy.get_robot_status()
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '!!fail indy get robot status')
                raise
            else:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), indy_status)

                val1 = indy.read_direct_variable(0, 601) #주문갯수
                val2 = indy.read_direct_variable(0, 602) #남은갯수
                val3 = indy.read_direct_variable(0, 611) #상태완료

                if(indy_status['ready'] == 1 and indy_status['error'] == 0 and indy_status['busy'] == 0):
                    indy_send_status = "Ready"
                if(indy_status['busy'] == 1):
                    indy_send_status = "Busy"
                if(indy_status['error'] == 1):
                    indy_send_status = "Error"
                if(indy_status['zero'] == 1):
                    indy_send_status = "Zero"
                if(indy_status['home'] == 1):
                    indy_send_status = "Home"
                # if(val1 > 0 and val2 == 0):
                #     indy_send_status = "Complate"

                print(time.strftime('%Y-%m-%d %H:%M:%S'), indy_send_status, "\n\n", "val :: ", val1, val2, "\n")

            val4 = "pause"

            try:
                indy_program_state = indy.get_program_state()

                if(indy_program_state["running"] == 1):
                    val4 = "running"
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '!!fail indy get program status')
                raise
            else:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), 'success indy get program status :: '.join(indy_program_state))

            stores = store_dao.find_store()
            storeid = ""

            for store in stores:
                print(store[1])
                storeid = store[1]

            device_dao.save_device(storeid, config.server_id, "NMRA", robot_name, val4 + "|" + str(val1) + "|" + str(val2) + "|" + str(val3), robot_name, indy_send_status, 100, 1)

            mq_util.send(config.mqnm, {
                "tp" : "nmrstatus",
                "id" : config.server_id,
                "ip" : config.ipin,
                "status" : indy_send_status,
                "pstatus" : val4 + "|" + str(val1) + "|" + str(val2) + "|" + str(val3),
                "robotid" : robot_name,
                "robotip" : robot_ip
            })
        try:
            indy.disconnect()
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '!!fail indy disconnect')
        else:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), 'success indy disconnect')

    except:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '!!fail socket connect ', sys.exc_info())
    else:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'success socekt connect')


    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(1)      #1초단위로 현재 상태 전달
