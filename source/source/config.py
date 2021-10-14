import getmac
import socket

server_id = "TR" + str(getmac.get_mac_address()).replace(":", "")
ipin = socket.gethostbyname(socket.gethostname())
ipout = socket.gethostbyname(socket.gethostname())

service_code = "TOD_TEST"

host = "3.36.46.213"
port = 8576
vhost = "/"
mqid = "robot"
mqpw = "robot2021!"
mqex = "TROBOT"
mqnm = "robot_main"

sqlite_host = "/robot/db/robot_210504.db"
#sqlite_host = "db/robot_210504.db"

vds_host = "http://3.36.46.213:8890/api"

nmr_ip = "192.168.103.230"  # Robot (Indy) IP
nmr_name = "NRMK-Indy7"  # Robot name (Indy7)