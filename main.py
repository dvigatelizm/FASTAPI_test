from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string, random
from fastapi.responses import RedirectResponse

app = FastAPI(title='URL-Shorter')

class URLItem(BaseModel):
    url: str

db = {}

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    #print(chars)
    while True:
        short_id = ''.join(random.choice(chars) for _ in renge(length))
        if short_id not in db:
            return short_id

@app.post("/shorter")
def shorter_url(item: URLItem):
    short_id = generate_short_id()
    db[short_id] = {"url": item.url, "clicks": 0}
    return {"short_url": f"http://127.0.0.1:8000/{short_id}"}

@app.get("/{short_id}")
def redirected_to_url(short_id: str):
    if short_id not in db:
        raise HTTPException(status_code=404, detail="URL not found")
    db[short_id]["clicks"] += 1
    return RedirectResponse(db[short_id]["url"])





#generate_short_url()




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app = FastAPI(title='To-Do-Serv')

# class Task(BaseModel):
#     title: str
#     completed: bool = False
#     deleted: bool = False 

# # Имитация БД
# tasks = {} # Пустой словарь с тасками
# # 'task1' : ['Сделать ДЗ по ПИ', True]
# task_id_counter = 1
# # POST /tasks – создание новой задачи

# @app.post("/tasks")
# def create_task(task: Task):
#     global task_id_counter
#     tasks[task_id_counter] = task
#     task_id_counter += 1
#     return {"id": task_id_counter - 1, "task": task}
    
# # GET /tasks – получение списка всех задач
# @app.get("/tasks")
# def get_all_tasks():
#     active = {
#         task_id: task for task_id, task in tasks.items()
#         if not task.deleted
#     }
#     return {"tasks": active}
# # GET /tasks/{id} – получение информации о конкретной задаче

# @app.get("/tasks/{task_id}") # GET / tasks/3 => get_task(task_id=5)
# def get_task(task_id: int):
#     if task_id not in tasks: # Есть ли задача с таким ID?
#         raise HTTPException(status_code=404, detail="Task not found")
#     return tasks[task_id]

# # PUT /tasks/{id} – обновление задачи (изменение текста или статуса)
# @app.put("/tasks/{task_id}")
# #  PUT/tasks/1
# # {'title' : "Купить хлеб И КЕФИР" , 'completed': true}
# def update_task(task_id: int, updated_task: Task):
#     if task_id not in tasks:
#         raise HTTPException(status_code=404, detail="Task for update not found")
#     tasks[task_id] = updated_task
#     return {"id": task_id, "task": updated_task}

# # DELETE /tasks/{id} – удаление задачи
# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int):
#     if task_id not in tasks:
#         raise HTTPException(status_code=404, detail="Task for delete not found")
#     # del tasks[task_id]
#     tasks[task_id].deleted = True
#     return {"status": "deleted"}