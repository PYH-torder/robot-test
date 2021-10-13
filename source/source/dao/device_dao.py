import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import sqlite3
import config

def save_device(store_id, ssid, rcode, device_id, etc, name, status, battery, rtype):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    # print(storeid + " / " + ssid + " / " + rcode + " / " + deviceid + " / " + etc + " / " + name + " / " + status + " / " + str(battery) + " / " + str(rtype))

    cur.execute("SELECT COUNT(*) FROM TB_DEVICE WHERE strDeviceid = ?", (device_id,))
    count = cur.fetchone()

    if count[0] > 0 :
        cur.execute("UPDATE TB_DEVICE SET strType = ?, strRobotinfo = ?, strName = ?, strStatus = ?, intBattery = ?, dateEdit = datetime('now', 'localtime'), intType = ?  WHERE strDeviceid = ?", (rcode, etc, name, status, battery, rtype, device_id))
    else :
        cur.execute("INSERT INTO TB_DEVICE (strType, strRobotinfo, strName, strStatus, intBattery, dateReg, dateEdit, strDeviceid, intType) VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'), ?, ?); ", (rcode, etc, name, status, battery, device_id, rtype))

    conn.commit()
    conn.close()

def find_device():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_DEVICE")
    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows

def delete_device(device_id):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("DELETE FROM TB_DEVICE WHERE strDeviceid = ?", (device_id,))

    conn.commit()
    conn.close()
