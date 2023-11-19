import requests
import re

import openai


openai.api_key = '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'
model = 'gpt-3.5-turbo-1106'

def gpt(query):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": query}],
        max_tokens=550
    )
    answer = response['choices'][0]['message']['content'].strip()
    return answer



def ordinance_from_gpt(x):
    user = x + "이 내용을 보고 독특한 조례를 3가지를 만들어서 리스트 형식으로 리턴해주세요."
    key_word = gpt(user)
    return key_word

def connect_from_gpt(x):
    user = x + "이 키워드를 보고 관련 있는 산업 분야 5가지를 리스트 형식으로 리턴해주세요. "
    new = gpt(user)
    return new

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
            "provider": [],
            "category": ["IT_과학"],
            "category_incident": ["재해>자연재해"],
            "byline": "",
           # "provider_subject": ["경제", "부동산"],
            "sort": {"date": "desc"},
            "hilight": 200,
            "return_from": 0,
            "return_size": 10,
            "fields": [
                "byline",
                "category",
                "category_incident",
                "provider_news_id",
                "provider_link_page"
                "content"
                "images"
            ]
        }
    }

    respone = requests.post(url, json=data)
    res = []
    if respone.status_code == 200:
        parsed_data = respone.json()
        for i in range(len(parsed_data['return_object']['documents'])):
            news_id = parsed_data['return_object']['documents'][i]['news_id']
            
            
            more = news_id_search([news_id])
            link = more['return_object']['documents'][0]['provider_link_page']
            content = more['return_object']['documents'][0]['content']
            images = more['return_object']['documents'][0]['images']
            byline = more['return_object']['documents'][0]['byline']

            title = parsed_data['return_object']['documents'][i]['title']
            hilight = remove_html_tags(parsed_data['return_object']['documents'][i]['hilight'])
            provider = parsed_data['return_object']['documents'][i]['provider']
            
            # keyword = create_keyword(parsed_data['return_object']['documents'][0]['title'], hilight)
            keyword = []
            # related_industry = related_industries(keyword, hilight)
            related_industry = []
            #AI 조례 생성
            #    created_ordinance = ordinance_from_gpt()
            res.append([provider, title, hilight, related_industry, link, content, images , byline])
        # print(res)
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
        return list(set(parsed_data['return_object']['result']['content'].split()))
    else:
        print("API 호출 실패", respone.status_code)
    

def news_id_search(id): #이 함수는 아이디 가지고 기사 분석 가능
    url = "https://tools.kinds.or.kr/search/news"

    data = {
        "access_key": "d66bd288-5a22-43d1-8db1-37fbfbd37b7f", 
        "argument": {
            "news_ids": id,#[ "01500701.2015083110018412570", "01100701.20150826100000152"],
            "fields": [
                "content",
                "byline",
                "images",
                "provider_link_page"
            ] 
        }
    }

    respone = requests.post(url, json=data)
    if respone.status_code == 200:
        parsed_data = respone.json()
        return parsed_data
    else:
        print("API 호출 실패", respone.status_code)


def related_industries(keyword, hilight):
    user = "키워드: "+str(keyword) + ", 내용: " + str(hilight) + "이야. 이 키워드와 내용을 분석해서 이 기사가 영향을 주는 산업 분야를 5가지로 파이썬 리스트를 만들어서 리스트만 리턴해줘"
    related = gpt(user)
    return related

# ordinance_from_gpt()

def select_cate(sex, age, job):
    # 남성과 여성의 관심사 리스트
    interests = {
        "M": {
            20: ["자동차", "IT_과학일반", "음악", "영화", "게임"],
            30: ["무역", "인터넷_SNS", "콘텐츠", "증권_증시", "외환"],
            40: ["의료_건강", "전시_공연", "미디어", "금융_재테크", "날씨"],
            50: ["부동산", "교육_시험", "서비스_쇼핑", "미디어", "취업_창업"]
        },
        "W": {
            20: ["여성", "출판", "취업_창업", "영화", "음악"],
            30: ["생활", "요리_여행", "날씨", "콘텐츠", "인터넷_SNS"],
            40: ["경제일반", "영화", "생활", "인터넷_SNS", "미디어"],
            50: ["미디어", "음악", "생활", "여행", "영화"]
        }
    }

    age_interests = interests.get(sex, {}).get(age, [])
    job_interests = {
        "학생": ["게임", "영화", "음악", "인터넷_SNS", "미디어"],
        "회사원": ["서비스_쇼핑", "증권_증시", "외환", "IT_과학일반", "인터넷_SNS"],
        "1차 산업": ["농구", "야구", "축구", "환경", "자원"],
        "공무원": ["행정_자치", "정치일반", "교육_시험", "외교", "사회일반"],
        "사업자": ["산업_기업", "자동차", "금융_재테크", "무역", "서비스_쇼핑"]
    }.get(job, [])

    return age_interests, job_interests

def find_common_interests(sex, age, job):
    age_list, job_list = select_cate(sex, age, job)
    all_interests = age_list + job_list if age_list and job_list else age_list or job_list
    
    if not all_interests:
        return []

    interests_count = {}
    for interest in all_interests:
        if interest in interests_count:
            interests_count[interest] += 1
        else:
            interests_count[interest] = 1

    sorted_interests = sorted(interests_count.items(), key=lambda x: x[1], reverse=True)
    top_interests = [item[0] for item in sorted_interests[:5]]

    return top_interests

