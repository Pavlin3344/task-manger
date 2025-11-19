import time
import sqlite3

def start_cleanup_worker():
    while True:
        db = sqlite3.connect("tasks.db")
        db.execute(
            "DELETE FROM tasks WHERE done = 1 AND created_at <= datetime('now', '-1 day')"
        )
        db.commit()
        db.close()
        time.sleep(60)

