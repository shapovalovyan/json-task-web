import json
import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class Priority(str, Enum):
    High = "High"
    Medium = "Medium"
    Low = "Low"


class TodoCreate(BaseModel):
    title: str
    priority: Priority = Priority.Low
    deadLine: str  # ISO datetime string
    completed: bool = False


class TodoUpdate(BaseModel):
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    priority: Priority
    deadLine: str
    completed: bool


# ===== Инициализация приложения =====
app = FastAPI(title="Todo API")

# CORS – разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TODOS_FILE = "data/todos.json"

def migrate_todos():
    """Добавляет недостающие поля priority и deadLine в существующие задачи."""
    with open(TODOS_FILE, "r", encoding="utf-8") as f:
        todos = json.load(f)
    
    updated = False
    for todo in todos:
        if "priority" not in todo:
            todo["priority"] = "Low"
            updated = True
        if "deadLine" not in todo:
            # Устанавливаем дедлайн на +1 день от текущего момента
            todo["deadLine"] = (datetime.now() + timedelta(days=1)).isoformat()
            updated = True
    
    if updated:
        with open(TODOS_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
        print("✅ Данные успешно мигрированы (добавлены priority и deadLine к старым задачам, если они есть)")


def ensure_todos_file():
    """Создаёт файл с одной задачей по умолчанию, если его нет."""
    if not os.path.exists(TODOS_FILE):
        os.makedirs(os.path.dirname(TODOS_FILE), exist_ok=True)
        with open(TODOS_FILE, "w", encoding="utf-8") as f:
            json.dump([{
                "id": 1,
                "title": "Первая задача",
                "priority": "Low",
                "deadLine": (datetime.now() + timedelta(days=1)).isoformat(),
                "completed": True
            }], f, ensure_ascii=False, indent=4)
    else:
        # Если файл существует, проверяем и мигрируем данные
        migrate_todos()


def read_todos() -> List[dict]:
    with open(TODOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_todos(data: List[dict]):
    with open(TODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.get("/todos", response_model=List[Todo])
async def get_todos():
    ensure_todos_file()
    return read_todos()


@app.post("/todos", response_model=List[Todo], status_code=201)
async def create_todo(todo: TodoCreate):
    ensure_todos_file()
    todos = read_todos()
    new_id = max([t["id"] for t in todos], default=0) + 1
    new_todo = {
            "id": new_id,
            "title": todo.title,
            "priority": todo.priority,
            "deadLine": todo.deadLine,
            "completed": todo.completed
        }
    todos.append(new_todo)
    write_todos(todos)
    print("✅ Данные успешно добавлены. Задача создана")
    return todos


@app.patch("/todos/{todo_id}", response_model=List[Todo])
async def patch_todo(todo_id: int, update: TodoUpdate):
    ensure_todos_file()
    todos = read_todos()
    for item in todos:
        if item["id"] == todo_id:
            if update.completed is not None:
                item["completed"] = update.completed
            write_todos(todos)
            print("✅ Данные успешно изменены.")
            return todos
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", response_model=List[Todo])
async def delete_todo(todo_id: int):
    ensure_todos_file()
    todos = read_todos()
    new_todos = [t for t in todos if t["id"] != todo_id]
    if len(new_todos) == len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    for idx, item in enumerate(new_todos, start=1):
        item["id"] = idx
    write_todos(new_todos)
    print("✅ Задача удалена")
    return new_todos