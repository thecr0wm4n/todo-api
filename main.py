from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    # The spec wants {"error": "..."} on every 4xx, not FastAPI's default {"detail": "..."}.
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: str = ""


# In-memory "database" — resets every time the server restarts.
tasks: list[Task] = [
    Task(id=1, title="Buy milk", done=False),
    Task(id=2, title="Write README", done=False),
    Task(id=3, title="Ship the API", done=True),
]
next_id = 4


def find_task(task_id: int) -> Task | None:
    return next((t for t in tasks if t.id == task_id), None)


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    global next_id
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    task = Task(id=next_id, title=payload.title.strip(), done=False)
    tasks.append(task)
    next_id += 1
    return task
