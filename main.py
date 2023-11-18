from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import bigkinds

app = FastAPI()
templates = Jinja2Templates(directory="template")

data2 = bigkinds.search_news()
data3 = bigkinds.news_id_search()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("article2.html", {"request": request, "data": data2})
    

@app.get("/data3")
async def read_root(request: Request):
    return templates.TemplateResponse("x.html", {"request": request, "data": data3})
    ## return 값을 html 에서 사용하려면 
    # {{ data.return_object.total_hits }} data.return_object사용

@app.get("/login")
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

