# Task API

A small CRUD API for managing a to-do list, built with FastAPI. Data lives in memory only — it resets every time the server restarts (that's intentional for this stage; a database comes later).

## What this is

Five endpoints covering the four CRUD operations (Create, Read, Update, Delete) on an in-memory list of tasks, plus a root endpoint and a health check. Interactive docs are generated automatically by FastAPI at `/docs`.

## How to run it

Requires Python 3.10+.

```bash
# from the repo root
pip install -r requirements.txt
uvicorn main:app --reload
```

The server starts on `http://localhost:8000`. Open `http://localhost:8000/docs` for interactive Swagger UI.

## Endpoints

| Method | Path           | Description                          | Success | Errors        |
|--------|----------------|---------------------------------------|---------|----------------|
| GET    | `/`            | API info                              | 200     | —              |
| GET    | `/health`      | Health check                          | 200     | —              |
| GET    | `/tasks`       | List all tasks                        | 200     | —              |
| GET    | `/tasks/{id}`  | Get a single task                     | 200     | 404 unknown id |
| POST   | `/tasks`       | Create a task (`{"title": "..."}`)    | 201     | 400 empty/missing title |
| PUT    | `/tasks/{id}`  | Replace a task's title/done           | 200     | 404 unknown id, 400 empty title |
| DELETE | `/tasks/{id}`  | Remove a task                         | 204     | 404 unknown id |

All errors return a JSON body shaped like `{"error": "message"}`.

## Example

```
$ curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

`/docs` lists every endpoint with a working "Try it out" for the full CRUD cycle.

![Swagger UI screenshot](swagger-screenshot.jpg)

*(Screenshot placeholder — replace `swagger-screenshot.png` with your own screenshot of `http://localhost:8000/docs` after running the server locally.)*

## The mortality experiment

*(Optional extra — after creating a few tasks and restarting the server, write two sentences here about what happened to the data and why. This is the setup for Week 3.)*