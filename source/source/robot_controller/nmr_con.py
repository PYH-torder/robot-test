import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from indy_utils import indydcp_client as client
import config

robot_ip = config.nmr_ip  # Robot (Indy) IP
robot_name = config.nmr_name  # Robot name (Indy7)

def start(programid):

    rtnvalue = 1

    try:
        indy = client.IndyDCPClient(robot_ip, robot_name)
        indy.connect()
    except:
        rtnvalue = 9
        indy.disconnect()
    else:
        indy.set_default_program(int(programid))
        indy.start_default_program()

        indy.disconnect()

    return rtnvalue



def stop(programid):

    rtnvalue = 1

    try:
        indy = client.IndyDCPClient(robot_ip, robot_name)
        indy.connect()
    except:
        rtnvalue = 9
        indy.disconnect()
    else:
        indy.set_default_program(int(programid))
        indy.stop_current_program()

        indy.disconnect()

    return rtnvalue

################### program
# code : 610
# value ::  1 : home
#           2 : marker left
#           10 : marker right
#           3 : ice cup
#           4 : hot cup
#           5 : coffee hot robot
#           11 : coffee ice robot
#           6 : ade robot
#           7 : drink on left serving robot
#           8 : drink on table
#           9 : drink on right serving robot

def set_var(programid, code, value):

    rtnvalue = 1

    try:
        indy = client.IndyDCPClient(robot_ip, robot_name)
        indy.connect()
    except:
        rtnvalue = 9
        indy.disconnect()
    else:
        indy.set_default_program(int(programid))
        indy.write_direct_variable(0, int(code), int(value))
        indy.disconnect()

    return rtnvalue