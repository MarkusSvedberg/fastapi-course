from fastapi import FastAPI, status
from todoapp import models
from todoapp.database import engine
from todoapp.routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def home_page_redirect():
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy", status_code=status.HTTP_200_OK)
async def health_check():
    return { "status": "healthy" }

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
