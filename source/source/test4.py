import requests
import config
from robot_controller import vd_con

#print(vd_con.status('9686649074951', 'c0847d1894e6'))

res = requests.post(config.vds_host + "/robot/action", json={
                    "deviceId" : '9686649074951',
                    "robotId" : 'c0847d1894e6',
                    "action" : "Complete"
                })
print(res)