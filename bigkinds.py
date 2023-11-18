import requests
import json

url = "https://tools.kinds.or.kr/search/news"

data = {           
    "access_key": "d66bd288-5a22-43d1-8db1-37fbfbd37b7f",
    "argument": {
        "query": "서비스 AND 출시",
        "published_at": {
            "from": "2019-01-01",
            "until": "2019-03-31"
        },
        "provider": ["경향신문"],
        "category": ["정치>정치일반", "IT_과학"],
        "category_incident": ["범죄", "교통사고", "재해>자연재해"],
        "byline": "",
        "provider_subject": ["경제", "부동산"],
        "subject_info": [""],
        "subject_info1": [""],
        "subject_info2": [""],
        "subject_info3": [""],
        "subject_info4": [""],
        "sort": {"date": "desc"},
        "hilight": 200,
        "return_from": 0,
        "return_size": 5,
        "fields": [
            "byline",
            "category",
            "category_incident",
            "provider_news_id"
        ]
    }
}

respone = requests.post(url, json=data)
if respone.status_code == 200:
    parsed_data = respone.json()
    print(parsed_data)

    
else:
    print("API 호출 실패", respone.status_code)