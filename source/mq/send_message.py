import requests
import json
import config

def send(robot_id, store_code, table_name, status):
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    data = {
        "robotId": robot_id,
        "storeCode": "TOD_TEST",
        "tableName": table_name,
        "status": status,
        "ssid": config.serverid
    }
    print(data)
    requests.post("http://demo.api.torder.co.kr/message/robotCommingForTable", headers = headers, data = json.dumps(data))