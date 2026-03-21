from fastapi import FastAPI
from app.tasks import process_task
from pydantic import BaseModel
from app.database import engine, Base
from app.models import Task
from app.database import SessionLocal

class TaskRequest(BaseModel):
    data: str

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/task")
def create_task(payload: TaskRequest):
    db = SessionLocal()

    task = process_task.delay(payload.data)

    db_task = Task(
        id=task.id,
        data=payload.data,
        status="PENDING"
    )

    db.add(db_task)
    db.commit()

    return {"task_id": task.id}

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
