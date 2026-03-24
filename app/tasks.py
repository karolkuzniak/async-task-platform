from celery import Celery
import time
from app.database import SessionLocal
from app.models import Task

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
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