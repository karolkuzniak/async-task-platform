from celery import Celery
import time
from app.database import SessionLocal
from app.models import Task

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task(bind=True)
def process_task(self, task_id, data):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id.id).first()

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