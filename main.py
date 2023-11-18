
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app = FastAPI()

templates = Jinja2Templates(directory="template")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("article1.html", {"request": request}) 