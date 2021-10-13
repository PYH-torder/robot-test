import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import sqlite3
import config

def save_store(store_id, store_name): 
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("UPDATE TB_STORE SET strStoreID = ?, strStoreName = ? WHERE intSeq > 0; ", (store_id, store_name))
    
    conn.commit()
    conn.close()

def find_store(): 
    conn = sqlite3.connect(config.sqlite_host)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TB_STORE LIMIT 1;")

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows

