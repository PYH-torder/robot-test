import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import sqlite3
import config

def save_order(store_id, ssid, otype, ocode, omenu, oname, oqty, otable):
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

def save_change_order(ocode, step1, step2, step3, step4, status, oqty):
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("UPDATE TB_ORDER SET intStep1 = ?, intStep2 = ?, intStep3 = ?, intStep4 = ?, nStatus = ?, dateEdit = datetime('now', 'localtime'), intNowQty = ? WHERE strOrderCode = ?; ", (step1, step2, step3, step4, status, oqty, ocode))

    conn.commit()
    conn.close()

def find_order():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_ORDER ORDER BY intSeq ASC;")

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows

def find_one_order():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_ORDER WHERE nStatus < 9 ORDER BY intSeq ASC LIMIT 1;")

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows

def flush_order():
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("DELETE FROM TB_ORDER WHERE dateEdit < date('now', '-1 day') and nStatus = 9;")
    cur.execute('SELECT changes();')
    deleted_row_cnt = cur.fetchall()[0][0]

    conn.commit()
    conn.close()

    return deleted_row_cnt