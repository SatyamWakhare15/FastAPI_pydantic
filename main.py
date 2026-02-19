from fastapi import FastAPI, Request,status,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

templates = Jinja2Templates(directory="templates")

# Mock data for posts
posts: list[dict] = [
    {
        "id": 1,
        "author": "Saty Wakh",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is a great language",
        "content": "Python is great for development and learning purposes",
        "date_posted": "April 30, 2025",
    }
]

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request,"home.html",{"posts":posts,"title":"Home"}
    )

@app.get("/api/posts")
def get_posts():
    return posts
