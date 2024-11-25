import requests
import json
import pandas as pd
import time

# ID와 Secret 읽기 함수
def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                config[key.strip()] = value.strip()
    return config

# txt 파일 경로
config_path = r"C:\Users\ktmth\Desktop\naver_labs.txt"
config = load_config(config_path)

# ID와 Secret 가져오기
client_id = config['ID']
client_secret = config['SECRET']

# 네이버 쇼핑 검색 API 호출 함수
def search_shopping(query, display=100):
    url = f"https://openapi.naver.com/v1/search/shop.json?query={query}&display={display}&sort=sim"
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# 검색 키워드 정의 (상의, 하의, 외투)
categories = {
    "상의": ["티셔츠", "셔츠", "블라우스", "니트", "후드티"],
    "하의": ["청바지", "슬랙스", "스커트", "레깅스"],
    "외투": ["재킷", "코트", "패딩"]
}

# 데이터 수집
results = []
for category, keywords in categories.items():
    for keyword in keywords:
        print(f"'{keyword}' 데이터 수집 중...")
        data = search_shopping(keyword)
        if data:
            results.append({
                "카테고리": category,
                "키워드": keyword,
                "검색량": len(data['items']),  # 검색 결과 수
                "날짜": pd.Timestamp.now()  # 수집 시점 기록
            })
        time.sleep(1)  # 요청 간 딜레이

# 데이터프레임 생성
df = pd.DataFrame(results)

# 저장
df.to_csv("fashion_search_data.csv", index=False, encoding="utf-8-sig")
print("데이터 저장 완료")
