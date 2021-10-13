import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pika
import json
import config
from dao import device_dao
from dao import order_dao
from dao import store_dao
from util import http_util

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=config.host
    , port=config.port
    , virtual_host=config.vhost
    , credentials=pika.PlainCredentials(config.mqid, config.mqpw)   # username, password
))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    if str(body) != None and str(body) != "":
        data = json.loads(body)
        if "ty" in data:
            print(" json :: %r " % data["ty"])

            #store save
            if(data["ty"] == "store"):
                store_dao.save_store(data["storeid"], data["storename"])

            #device set
            if(data["ty"] == "device"):
                device_dao.save_device(data["storeid"], data["ssid"], data["rcode"], data["deviceid"], data["etc"], data["name"], data["status"], data["battery"], data["rtype"])

            if(data["ty"] == "devicedel"):
                device_dao.delete_device(data["deviceid"])

            #order set
            if(data["ty"] == "order"):
                order_dao.save_order(data["storeid"], data["ssid"], data["otype"], data["ocode"], data["omenu"], data["oname"], data["oqty"], data["otable"])
            
            if(data["ty"] == ""):
                pass

            sys.stdout.flush()

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.queue_declare(queue=config.server_id)
channel.basic_consume(config.server_id, callback)
print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
channel.start_consuming()