from fastapi import FastAPI, Depends, status
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import model
from typing import List
from schemas import Todos, Categories


model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="To-Do Application",
    description="Todo Application developed with FastAPI for the basic CRUD operations",
    version="1.0.0",
)


@app.post('/todo', tags=['Tasks'])
async def create_task(request: schemas.Todos, db: Session = Depends(get_db)):
    create_new = model.Todos(tasks=request.tasks, cat_id=1)
    db.add(create_new)
    db.commit()
    return "A new task has been created successfully"


@app.get('/todo', tags=['Tasks'], response_model=List[schemas.DisplayTodos])
async def view_all_tasks(db: Session = Depends(get_db)):
    all_tasks = db.query(model.Todos).all()
    if all_tasks:
        return all_tasks
    else:
        return "List is presently empty."


@app.get('/todo/{id}', tags=['Tasks'])
async def view_a_task(id, db: Session = Depends(get_db)):
    get_task = db.query(model.Todos).filter(model.Todos.id == id).first()
    if get_task:
        return get_task
    else:
        return f"Task with an ID of {id} does not exist in the list"


@app.put('/todo/{id}', tags=['Tasks'])
async def update_task(id, request: schemas.Todos, db: Session = Depends(get_db)):
    task_update = db.query(model.Todos).filter(model.Todos.id == id).update({"tasks": request.tasks})
    db.commit()
    if task_update:
        return f"Task with the ID of {id} has been updated!"
    else:
        return f"Task with an ID of {id} does not exist in the list"


@app.delete('/todo/{id}', tags=['Tasks'])
async def complete_a_task(id, db: Session = Depends(get_db)):
    complete = db.query(model.Todos).filter(model.Todos.id == id).first()
    db.delete(complete)
    db.commit()
    return f"Task with the ID of {id} has been completed, hence removed!"


@app.post('/categories', tags=['Task Categories'])
async def create_category(request: schemas.Categories, db: Session = Depends(get_db)):
    create_new = model.Categories(categories=request.categories)
    db.add(create_new)
    db.commit()
    return "A new Task Category has been created"


@app.delete('/categories/{id}', tags=['Task Categories'])
async def remove_a_category(id, db: Session = Depends(get_db)):
    remove = db.query(model.Categories).filter(model.Categories.id == id).first()
    if remove:
        db.delete(remove)
        db.commit()
        return "A task category has been deleted"
    else:
        return "Task category does not exist"


@app.get('/categories', tags=['Task Categories'])
async def view_all_categories(db: Session = Depends(get_db)):
    all_categories = db.query(model.Categories).all()
    if all_categories:
        return all_categories
    else:
        return "No Task category found!"


@app.put('/categories/{id}', tags=['Task Categories'])
async def update_category(id, request: schemas.Categories, db: Session = Depends(get_db)):
    update_cat = db.query(model.Categories).filter(model.Categories.id == id).update(
        {'categories': request.categories}
    )
    if update_cat:
        db.commit()
        return f"Task category with the ID of {id} has been updated successfully!"
    else:
        return "Task category not found!"
