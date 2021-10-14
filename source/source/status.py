import time
import config
from mq_util import mq_util

while True:

    mq_util.send(config.mqnm, {
        "tp" : "status",
        "id" : config.server_id,
        "ip" : config.ipin
    })

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(30)      #30초단위로 현재 상태 전달