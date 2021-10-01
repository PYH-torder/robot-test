import sqlite3
import config

def setStore(storeid, storename):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("UPDATE TB_STORE SET strStoreID = ?, strStoreName = ? WHERE intSeq > 0; ", (storeid, storename))
    
    conn.commit()
    conn.close()

def getStore():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_STORE LIMIT 1;")

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows


def setDevice(storeid, ssid, rcode, deviceid, etc, name, status, battery, rtype):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    # print(storeid + " / " + ssid + " / " + rcode + " / " + deviceid + " / " + etc + " / " + name + " / " + status + " / " + str(battery) + " / " + str(rtype))

    cur.execute("SELECT COUNT(*) FROM TB_DEVICE WHERE strDeviceid = ?", (deviceid,))
    count = cur.fetchone()

    if count[0] > 0 :
        cur.execute("UPDATE TB_DEVICE SET strType = ?, strRobotinfo = ?, strName = ?, strStatus = ?, intBattery = ?, dateEdit = datetime('now', 'localtime'), intType = ?  WHERE strDeviceid = ?", (rcode, etc, name, status, battery, rtype, deviceid))
    else :
        cur.execute("INSERT INTO TB_DEVICE (strType, strRobotinfo, strName, strStatus, intBattery, dateReg, dateEdit, strDeviceid, intType) VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'), ?, ?); ", (rcode, etc, name, status, battery, deviceid, rtype))

    conn.commit()
    conn.close()

def getDevice():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_DEVICE")
    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows


def delDevice(deviceid):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("DELETE FROM TB_DEVICE WHERE strDeviceid = ?", (deviceid,))

    conn.commit()
    conn.close()


def setOrder(storeid, ssid, otype, ocode, omenu, oname, oqty, otable):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM TB_ORDER WHERE strOrderCode = ?; ", (ocode,))
    count = cur.fetchone()
    
    if count[0] > 0 :
        cur.execute("UPDATE TB_ORDER SET strOrderName = ?, strOrderMenu = ?, intType = ?, intOrderQty = ?, dateEdit = datetime('now', 'localtime'), strTableName = ? WHERE strOrderCode = ?; ", (oname, omenu, otype, oqty, otable, ocode))
    else :
        cur.execute("INSERT INTO TB_ORDER (intType, strOrderCode, strOrderName, strOrderMenu, intStep1, intStep2, intStep3, intStep4, nStatus, dateReg, dateEdit, intOrderQty, strTableName) VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0, datetime('now', 'localtime'), datetime('now', 'localtime'), ?, ?); ", (otype, ocode, oname, omenu, oqty, otable))

    conn.commit()
    conn.close()


def setChangeOrder(ocode, step1, step2, step3, step4, status, oqty):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("UPDATE TB_ORDER SET intStep1 = ?, intStep2 = ?, intStep3 = ?, intStep4 = ?, nStatus = ?, dateEdit = datetime('now', 'localtime'), intNowQty = ? WHERE strOrderCode = ?; ", (step1, step2, step3, step4, status, oqty, ocode))

    conn.commit()
    conn.close()


def getOrderOne():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_ORDER WHERE nStatus < 9 ORDER BY intSeq ASC LIMIT 1;")

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows

def getOrder():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_ORDER ORDER BY intSeq ASC;")

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows


def getReadyRobot(type):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

def flushDb(): 
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("DELETE FROM TB_ORDER WHERE dateEdit < date('now', '-1 day') and nStatus = 9;")
    cur.execute('SELECT changes();')
    deleted_row_cnt = cur.fetchall()[0][0]

    conn.commit()
    conn.close()

    return deleted_row_cnt