import requests

# ID와 SECRET 읽기 함수
def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.strip().split(':', 1)  # ':' 기준으로 분리
                config[key.strip()] = value.strip()
    return config

# txt 파일 경로
config_path = r"C:\Users\ktmth\Desktop\naver_labs.txt"
config = load_config(config_path)

# ID와 Secret 가져오기
client_id = config['ID']
client_secret = config['SECRET']

# 검색어 설정
query = '티셔츠'

# 요청 URL
url = f'https://openapi.naver.com/v1/search/shop.json?query={query}&display=10&start=1&sort=sim'

# 요청 헤더
headers = {
    'X-Naver-Client-Id': client_id,
    'X-Naver-Client-Secret': client_secret
}

# API 호출
response = requests.get(url, headers=headers)

# 응답 처리
if response.status_code == 200:
    data = response.json()
    for item in data['items']:
        print(f"상품명: {item['title']}, 가격: {item['lprice']}원")
else:
    print(f"Error Code: {response.status_code}")
