
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# app = FastAPI()
# templates = Jinja2Templates(directory="template")

# @app.get("/")
# async def read_root(request: Request):
#     return templates.TemplateResponse("article2.html", {"request": request})

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import bigkinds

app = FastAPI()
templates = Jinja2Templates(directory="template")

data2 = bigkinds.search_news()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("article2.html", {"request": request, "data": data2})

