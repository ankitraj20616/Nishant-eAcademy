from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from os.path import dirname, join
from routers import router
from database import Engine
import store


current_dir = dirname(__file__)  # this will be the location of the current .py file
static = join(current_dir, 'static')
templates = join(current_dir, 'templates')

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory=static), name= "static")
templates = Jinja2Templates(directory=templates)
store.Base.metadata.create_all(bind= Engine)

app.include_router(router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 