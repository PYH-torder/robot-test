import time
import config
from mq_util import mq_util

queue2 = "robot_main"

while True:

    mq_util.send(queue2, {
        "tp" : "status",
        "id" : config.server_id,
        "ip" : config.ipin
    })

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(30)      #30초단위로 현재 상태 전달