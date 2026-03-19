from fastapi import FastAPI
from app.tasks import process_task

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/task")
def create_task(data: str):
    task = process_task.delay(data)
    return {"task_id": task.id}
