import pika
import time
import config
import setmq

queue2 = "robot_main"

while True:

    setmq.send(queue2, {
        "tp" : "status",
        "id" : config.serverid,
        "ip" : config.ipin
    })

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(30)      #30초단위로 현재 상태 전달