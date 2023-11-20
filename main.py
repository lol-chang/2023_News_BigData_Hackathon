
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import bigkinds

app = FastAPI()
templates = Jinja2Templates(directory="template")

# data2 = bigkinds.search_news()
# data3 = bigkinds.news_id_search()
#data4 = bigkinds.search_test()
#print(data4)

# 회원가입 정보 KEY값 =============
user_age = 20
user_job ="None"
user_gender="Undefined";    2   
user_country="서울(기본값)"
# ================================

@app.get("/")
async def read_root(request: Request):  
    return templates.TemplateResponse("article2.html", {"request": request , "age": user_age,"job": user_job, "gender": user_gender , "country": user_country})
    

# @app.get("/data3")
# async def read_root(request: Request):
#     return templates.TemplateResponse("x.html", {"request": request, "data": data3})
    ## return 값을 html 에서 사용하려면 
    # {{ data.return_object.total_hits }} data.return_object사용
@app.get("/search")
async def show_login(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})
@app.get("/login")
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.get("/plaza")
async def show_login(request: Request):
    return templates.TemplateResponse("plaza.html", {"request": request})

@app.get("/debate")
async def show_login(request: Request):
    return templates.TemplateResponse("debate.html", {"request": request})


@app.get("/user_info")
async def read_root(request: Request):  
    return templates.TemplateResponse("user_info.html", {"request": request, "age": user_age,"job": user_job, "gender": user_gender , "country": user_country})


start = True
global_data = []

@app.get("/get_data")
async def get_data():
    global global_data, start
    if start:
        global_data = bigkinds.make_news(tmp)
        start = False
    data = global_data
    return data

tmp = []

@app.post("/server")
async def get_data(age: int = Form(...) , gender : str = Form(...) , job : str = Form(...) , region : str = Form(...) ):
    global user_age, user_gender , user_job ,user_country
    user_age = age
    user_job = job
    user_gender = gender
    user_country= region
    global tmp

    tmp = bigkinds.select_cate(gender, age, job)
    # 예시 응답
    return {"message": "Data received successfully"}


