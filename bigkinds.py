import requests
import re
import openai
import ast


model = 'text-davinci-003'

def gpt(query):
    response = openai.Completion.create(
        engine=model,
        prompt=query,
        max_tokens=2000
    )
    answer = response['choices'][0]['text']
    return answer


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
                  
global_related = []
first = True
def search_news(x,y,k,last=False):
    global global_related, first
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
            "category": x,
            "category_incident": y,
            "byline": "",
           # "provider_subject": ["경제", "부동산"],
            "sort": {"date": "desc"},
            "hilight": 200,
            "return_from": 0,
            "return_size": k,
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
            
            keyword = create_keyword(title, hilight)

            # global_related.append(keyword)
            global_related.append(hilight)

            related_industry = []
            #AI 조례 생성
            #    created_ordinance = ordinance_from_gpt()
            res.append([provider, title, hilight, related_industry, link, content, images , byline])
        # if last:
        #     related_industries()
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
            "news_ids": id,
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


def related_industries():
    res = []
    global global_related

    sliced_list = [global_related[i:i+2] for i in range(0, len(global_related), 2)]
    
    for i in range(3):
        user = str(sliced_list[i]) + "리스트 구조의 인덱스 마다 다른 기사야. 각각의 기사의 키워드를 보고 기사에 연관있는 산업 카테고리 이름 3개랑 기사에서 제시하는 문제점를 해결하기 위한 독특한 조례 무조건 2가지를 각각의 문자열 길이을 2줄 정도로 리턴해줘, 특히 조례를 좀 길게 해줘. 무조건 관련산업분야1 /관련 산업 분야2 / 관련산업분야3 / 조례1 / 조례2 다음 줄에 관련산업분야1 /관련산업분야2 / 관련산업분야3 / 조례1 / 조례2 이런 형식으로 아무 말 없이 이 형식으로만 값들을 리턴해. "
        key_word = gpt(user)
        print(key_word)
    
    
    # return res

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

    return list(set(age_interests + job_interests))

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


news = []
def make_news(tmp):
    # 사건사고 뉴스 추가 
    global news
    news = search_news(["사건_사고"], ["범죄"], 2)
    
    # 정치 뉴스 추가 
    for i in search_news(["정치"], ["범죄"], 2):
        news.append(i)
    
    #관심 뉴스 추가 
    state = True
    for i in search_news(tmp, ["범죄"], 2, last=state):
        news.append(i)
    
    return news
