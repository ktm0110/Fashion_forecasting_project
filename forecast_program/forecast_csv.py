import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
from prophet import Prophet

# Matplotlib 백엔드 설정 (Tkinter 오류 방지)
import matplotlib
matplotlib.use('Agg')

# 데이터 파일 경로
files = {
    "Top": "Top.csv",
    "Material": "Material.csv",
    "Outerwear": "Outerwear.csv",
    "Bottom": "Bottom.csv",
    "LookType": "LookType.csv"
}

# 데이터 정리 함수
def clean_data(df, key):
    clean_df = df.iloc[:, [0] + list(range(1, len(df.columns), 2))]
    clean_df.columns = ['Date'] + [f"{key}_{col}" for col in clean_df.columns[1:]]
    clean_df.loc[:, 'Date'] = pd.to_datetime(clean_df['Date'], errors='coerce')
    return clean_df.dropna(subset=['Date'])

# 각 파일 정리
dataframes = {}
for key, path in files.items():
    df = pd.read_csv(path)
    dataframes[key] = clean_data(df, key)

# 모든 데이터를 날짜를 기준으로 병합
merged_data = reduce(
    lambda left, right: pd.merge(left, right, on="Date", how="outer"),
    dataframes.values()
)

# 카테고리별 데이터 추출
categories = {
    "Clothing": [col for col in merged_data.columns if col.startswith(("Top", "Bottom", "Outerwear"))],
    "LookType": [col for col in merged_data.columns if col.startswith("LookType")],
    "Material": [col for col in merged_data.columns if col.startswith("Material")],
}

# 각 카테고리에 대한 그래프 생성 및 예측 데이터 저장
for category_name, columns in categories.items():
    plt.figure(figsize=(12, 6))
    for column in columns:
        # 데이터 준비
        category_data = merged_data[['Date', column]].dropna()
        prophet_data = category_data.rename(columns={'Date': 'ds', column: 'y'})

        # Prophet 모델 생성 및 학습
        model = Prophet()
        model.fit(prophet_data)

        # 미래 데이터 생성 및 예측
        future = model.make_future_dataframe(periods=365)  # 1년 예측
        forecast = model.predict(future)

        # 기존 데이터 플롯
        plt.plot(category_data['Date'], category_data[column], label=f"{column} (Actual)")

        # 예측 데이터 플롯
        plt.plot(forecast['ds'], forecast['yhat'], '--', label=f"{column} (Forecast)")

        # 예측 데이터를 CSV로 저장
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(
            f"{category_name}_{column}_forecast.csv", index=False, encoding='utf-8-sig'
        )

    plt.title(f"{category_name} Categories Trend with Forecast")
    plt.xlabel("Date")
    plt.ylabel("Search Volume (Relative)")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig(f"{category_name}_trend_with_forecast.png")
    plt.close()

print("All combined trend plots with forecasts have been saved, and forecast data exported to CSV.")
