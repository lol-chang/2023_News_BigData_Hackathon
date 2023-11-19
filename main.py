
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import bigkinds

app = FastAPI()
templates = Jinja2Templates(directory="template")

data2 = bigkinds.search_news()
# data3 = bigkinds.news_id_search()
#data4 = bigkinds.search_test()
#print(data4)

# 회원가입 정보 KEY값 =============
user_age = 20
user_job ="???"
user_gender="";    
user_country="서울"
# ================================

@app.get("/")
async def read_root(request: Request):  
    return templates.TemplateResponse("article2.html", {"request": request, "data": data2 , "age": user_age,"job": user_job, "gender": user_gender , "country": user_country})
    

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

@app.get("/get_data")
async def get_data():
    # 여기에서 데이터를 가져오는 로직을 구현하고 데이터를 반환합니다.
    # 이 부분은 실제 데이터를 가져오는 로직으로 대체되어야 합니다.
    data = bigkinds.search_news()
      # 예시 데이터
    return data



@app.post("/server")
async def get_data(age: int = Form(...) , gender : str = Form(...) , job : str = Form(...) , region : str = Form(...) ):
    global user_age, user_gender , user_job ,user_country
    user_age = age
    user_job = job
    user_gender = gender
    user_country= region
    # 예시 응답
    return {"message": "Data received successfully"}


