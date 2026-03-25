from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.tasks import process_task
from pydantic import BaseModel
from app.database import engine, Base
from app.models import Task
from app.database import SessionLocal
from sqlalchemy.exc import OperationalError
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import uuid
import time

app = FastAPI()

class TaskRequest(BaseModel):
    data: str

for i in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        print("DB not ready, retrying... ")
        time.sleep(2)

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

    db.close()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task.id,
        "status": task.status,
        "result": task.result,
        "data": task.data
    }

@app.middleware("http")
async def metrics_middleware(request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

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
                "result": t.result,
                "data": t.data
            }
            for t in tasks
        ]
    finally:
        db.close()

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")