import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import config
import pika

def send(quename, json):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=config.host
        , port=config.port
        , virtual_host=config.vhost
        , credentials=pika.PlainCredentials(config.mqid, config.mqpw)   # username, password
    ))
    channel = connection.channel()
    channel.queue_declare(queue=quename)

    channel.basic_publish(
        exchange=''             # 다른 Queue로 Routing하는 역할
        , routing_key=quename     # Message를 적재할 Queue
        , body=str(json)          # 전송할 Message
    )

    connection.close()