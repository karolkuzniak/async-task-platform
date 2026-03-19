from celery import Celery
import time

celery = Celery(
    "worker"
    broker="redis://localhost:6379/0"
    backend="redis://localhost:6379/0"
)

@celery.task
def process_task(data):
    time.sleep(5)
    return f"Processed: {data}"