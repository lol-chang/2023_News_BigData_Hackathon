import openai

openai.api_key = '#### KEY 보안 유지 #####'

# 모델을 변경을 해야 할지? 
model = "text-davinci-003"

# 질문 작성하기
query = "fast api 프로젝트 배포 방법 알려줘"

response = openai.Completion.create(
  engine=model,
  prompt=query,
  max_tokens=550 #글자수 제한
)
answer = response.choices[0].text.strip()
print(answer)
