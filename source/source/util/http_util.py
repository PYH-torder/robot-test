import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import requests
import json

def send_notification(robot_id, store_code, table_name, status, ssid):
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    data = {
        "robotId": robot_id,
        "storeCode": store_code,
        "tableName": table_name,
        "status": status,
        "ssid": ssid
    }
    
    requests.post("http://demo.api.torder.co.kr/message/robotCommingForTable", headers = headers, data = json.dumps(data))