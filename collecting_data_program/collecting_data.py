from pytrends.request import TrendReq
import pandas as pd

# 객체 생성
pytrends = TrendReq(hl='ko-KR', tz=540)

# 검색 키워드 분류 - 상의, 하의, 신발
keywords = {
    "상의": ["티셔츠", "셔츠", "블라우스", "니트", "후드티", "재킷", "코트", "패딩"],
    "하의": ["청바지", "슬랙스", "반바지", "스커트", "레깅스"],
    "신발": ["운동화", "구두", "샌들", "슬리퍼", "부츠"]
}

# 데이터프레임 초기화
all_data = pd.DataFrame()

# 카테고리별 데이터 수집
for category, words in keywords.items():
    for word in words:
        pytrends.build_payload([word], cat=0, timeframe='today 5-y', geo='KR', gprop='')
        data = pytrends.interest_over_time()

        if not data.empty:
            data = data.drop(labels=['isPartial'], axis='columns')
            data["카테고리"] = category
            data["키워드"] = word

            # 결과 합치기
            all_data = pd.concat([all_data, data])

# 저장
all_data.to_csv("fashion_trends.csv", encoding='utf-8-sig')
print("데이터 저장 완료")
