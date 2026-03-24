from fastapi import FastAPI
from app.tasks import process_task
from pydantic import BaseModel
from app.database import engine, Base
from app.models import Task
from app.database import SessionLocal
import uuid
import time
from sqlalchemy.exc import OperationalError
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response


class TaskRequest(BaseModel):
    data: str

for i in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        print("DB not ready, retrying... ")
        time.sleep(2)

app = FastAPI()

REQUEST_COUNT = Counter("app_request_total", "Total request")
REQUEST_TIME = Histogram("app_request_duration_seconds", "Request duration")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/task")
def create_task(payload: TaskRequest):
    db = SessionLocal()

    try:
        task_id = str(uuid.uuid4())

        db_task = Task(
            id=task_id,
            data=payload.data,
            status="PENDING"
        )

        db.add(db_task)
        db.commit()

        process_task.delay(task_id, payload.data)

        return {"task_id": task_id}

    finally:
        db.close()

@app.get("/task/{task_id}")
def get_task(task_id: str):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    return {
        "id": task.id,
        "status": task.status,
        "result": task.result
    }

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    REQUEST_COUNT.inc()
    REQUEST_TIME.observe(duration)

    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.get("/tasks")
def list_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()

        return [
            {
                "id": t.id,
                "status": t.status,
                "result": t.result
            }
            for t in tasks
        ]
    finally:
        db.close()