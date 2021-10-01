import pika
import json
import config
import setdb

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
                setdb.setStore(data["storeid"], data["storename"])

            #device set
            if(data["ty"] == "device"):
                setdb.setDevice(data["storeid"], data["ssid"], data["rcode"], data["deviceid"], data["etc"], data["name"], data["status"], data["battery"], data["rtype"])

            if(data["ty"] == "devicedel"):
                setdb.delDevice(data["deviceid"])

            #order set
            if(data["ty"] == "order"):
                setdb.setOrder(data["storeid"], data["ssid"], data["otype"], data["ocode"], data["omenu"], data["oname"], data["oqty"], data["otable"])

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.queue_declare(queue=config.serverid)
channel.basic_consume(config.serverid, callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()