from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    age: int
    city: str

@app.post("/send_data")
async def send_data(item: Item):
    # 받은 데이터 처리
    return {"message": "Data received successfully"}
