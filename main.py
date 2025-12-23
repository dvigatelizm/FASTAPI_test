from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title='To-Do-Serv')

class Task(BaseModel):
    title: str
    completed: bool = False
    deleted: bool = False

tasks = {}

task_id_counter = 1

# POST /task
@app.post("/tasks")
def create_task(task: Task):
    global task_id_counter
    tasks[task_id_counter] = task
    task_id_counter += 1
    return {"id": task_id_counter-1, "task": task}

# GET /tasks
@app.get("/tasks")
def get_all_tasks():
    active = {
        task_id: task for task_id, task in tasks.items()
        if not task.deleted
    }
    return {"tasks": active}

# GET /Tasks/{id}
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

# PUT /tasks/{id}
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task for update not found")
    tasks[task_id] = updated_task
    return {"id": task_id, "task": updated_task}

# DELETE /task/{id}
@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task for delete not found")
    # del tasks[task_id]
    tasks[task_id].deleted = True
    #return {"id": task_id, "status": "deleted"}
    return {"status": "deleted"}

# GET /tasks/deleted
@app.get("/tasks/deleted")
def get_delete_tasks():
    deleted = {
        task_id: task for task_id, task in tasks.items()
        if tasks.deleted
    }
    return {"deleted_tasks": {deleted}}