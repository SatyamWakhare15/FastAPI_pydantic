from fastapi import FastAPI, Request,status,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate,PostResponse

app = FastAPI()



#app.mount("/static",StaticFiles(directory="static"),name="static")

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

@app.get("/posts/{post_id}",include_in_schema=False)
def post_page(request : Request,post_id : int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post":post,"title":title},

            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
@app.get("/api/posts",response_model = list[PostResponse])
def get_posts():
    return posts

##
## Create Post
@app.get(
    "/api/posts",
    response_model = PostResponse,
    status_code = status.HTTP_201_CREATED,

)
def create_post(post:PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author":post.author,
        "title" : post.title,
        "content" : post.content,
        "date_posted" : "April 23,2025",
    }
    posts.append(new_post)
    return new_post
##
@app.get("/api/posts/{post_id}",response_model = PostResponse)
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return post
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="Post not found")
    
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request:Request,exception:StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occured.Please check your request and try again."
    )

  #  @app.get => routes("/api/posts/{post_id}")