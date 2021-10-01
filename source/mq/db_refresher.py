from apscheduler.schedulers.blocking import BlockingScheduler
import time
import setdb

scheduler = BlockingScheduler()
SCHEDULED_HOUR = 0
SCHEDULED_MINUTE = 0

def flush_db():
    deleted_row_cnt = setdb.flushDb()
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'old record delete count :', deleted_row_cnt, flush=True)

scheduler.add_job(flush_db, 'cron', hour=SCHEDULED_HOUR, minute=SCHEDULED_MINUTE, id='flush_db')
print(time.strftime('%Y-%m-%d %H:%M:%S'), ' [*] db_refresher started. Runs every day at [',
    '{0:02d}'.format(SCHEDULED_HOUR),':','{0:02d}'.format(SCHEDULED_MINUTE),']. To exit press CTRL+C', flush=True)
scheduler.start()