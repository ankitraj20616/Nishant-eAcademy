from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import store
from routers import router
from database import Engine

app = FastAPI()
app.mount("/static", StaticFiles(directory = r"E:\Nishant-eAcademy\app\static"), name= "static")
templates = Jinja2Templates(directory=r"E:\Nishant-eAcademy\app\templates")
store.Base.metadata.create_all(bind= Engine)

app.include_router(router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("Login_Page.html", {"request": request}) 