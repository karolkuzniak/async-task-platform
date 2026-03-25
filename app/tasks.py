from celery import Celery
import time
from app.database import SessionLocal
from app.models import Task
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task
def process_task(task_id, data):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()

        if task:
            task.status = "STARTED"
            db.commit()

        time.sleep(5)

        result = f"Processed: {data}"

        if task:
            task.status = "SUCCESS"
            task.result = result
            db.commit()

        return result

    finally:
        db.close()
