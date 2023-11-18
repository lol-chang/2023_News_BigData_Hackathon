import requests
import json
import re


import openai
openai.api_key = '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'
# 모델을 변경을 해야 할지? 
model = "text-davinci-003"
# model= "gpt-3.5-turbo"
def gpt(query):
  # openai migrate 업데이트 필요함 
  response = openai.Completion.create(
    engine=model,
    prompt=query,
    max_tokens=550 #글자수 제한
  )
  answer = response.choices[0].text.strip()
  return answer

def ordinance_from_gpt(x):
    user = x + "이 내용을 보고 독특한 조례를 3가지를 만들어서 리스트 형식으로 리턴해주세요."
    key_word = gpt(user)
    print(key_word)

def connect_from_gpt(x):
    user = x + "이 키워드를 보고 관련 있는 산업 분야 5가지를 리스트 형식으로 리턴해주세요. "
    new = gpt(user)
    print(new)

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def search_news():
    url = "https://tools.kinds.or.kr/search/news"

    data = {           
        "access_key": "d66bd288-5a22-43d1-8db1-37fbfbd37b7f",
        "argument": {
            "query": "",
            "published_at": {
                "from": "2019-01-01",
                "until": "2023-03-31"
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
            "return_size": 1,
            "fields": [
                "byline",
                "category",
                "category_incident",
                "provider_news_id"
            ]
        }
    }

    respone = requests.post(url, json=data)
    res = []
    if respone.status_code == 200:
        parsed_data = respone.json()
        for i in parsed_data['return_object']['documents']:
            hilight = remove_html_tags(i['hilight'])
            keyword = create_keyword(i['title'], hilight)
            res.append([i['provider'], i['title'], hilight, keyword])
        return res
    else:
        print("API 호출 실패", respone.status_code)

#hilight 내용을 보고 키워드를 추출는 FUNC
def create_keyword(title, hilight):
    url = "https://tools.kinds.or.kr/keyword"
    data = { 
        "access_key": "d66bd288-5a22-43d1-8db1-37fbfbd37b7f",
            "argument": {
                "title": title, 
                "sub_title": "", 
                "content": hilight
            }
        }
    respone = requests.post(url, json=data)
    res = []
    if respone.status_code == 200:
        parsed_data = respone.json()
        print(list(parsed_data['return_object']['result']['content'].split()))
        # connect_from_gpt(parsed_data)
        # print("keyword: ", parsed_data)
    else:
        print("API 호출 실패", respone.status_code)
    

def news_id_search(): #이 함수는 아이디 가지고 기사 분석 가능
    url = "https://tools.kinds.or.kr/search/news"

    data = {
        "access_key": "d66bd288-5a22-43d1-8db1-37fbfbd37b7f", 
        "argument": {
            "news_ids": [ "01500701.2015083110018412570", "01100701.20150826100000152"],
            "fields": [
                "content",
                "byline",
                "category",
                "category_incident",
                "images",
                "provider_subject",
                "provider_news_id",
                "publisher_code"] 
        }
    }

    respone = requests.post(url, json=data)
    if respone.status_code == 200:
        parsed_data = respone.json()
        return parsed_data
    else:
        print("API 호출 실패", respone.status_code)

