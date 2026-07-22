from fastapi import FastAPI

app = FastAPI(title="Task API", version="1.0")

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    # The brief wants {"error": "..."} on every 4xx, not FastAPI's default {"detail": "..."}.
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


class Task(BaseModel):
    id: int
    title: str
    done: bool = False

class TaskCreate(BaseModel):
    title: str = ""

tasks: list[Task] = [
    Task(id=1, title="Buy milk", done=False),
    Task(id=2, title="Write README", done=False),
    Task(id=3, title="Ship the API", done=True),
]
next_id = 4

class TaskUpdate(BaseModel):
    title: str = ""
    done: bool = False

def find_task(task_id: int) -> Task | None:
    return next((t for t in tasks if t.id == task_id), None)

@app.get("/", summary="API info", description="Describes this API and lists its main resource.")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check", description="Confirms the server is alive.")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List tasks", description="Returns every task currently in memory.")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get one task", description="Returns a single task by id, or 404 if it does not exist.")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201, summary="Create a task", description="Creates a task from a title. Returns 400 if the title is missing or empty.")
def create_task(payload: TaskCreate):
    global next_id
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    task = Task(id=next_id, title=payload.title.strip(), done=False)
    tasks.append(task)
    next_id += 1
    return task


@app.put("/tasks/{task_id}", summary="Update a task", description="Replaces a task's title and done status. Returns 404 for an unknown id, 400 for an empty title.")
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    task.title = payload.title.strip()
    task.done = payload.done
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", description="Removes a task by id. Returns 404 if it does not exist.")
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
    return None