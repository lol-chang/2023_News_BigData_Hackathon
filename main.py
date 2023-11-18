
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="template")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("article2.html", {"request": request})


