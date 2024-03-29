import pandas as pd
# CSV 파일 경로
file_path = "daily_call_rate.csv"
# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv(file_path)
# '콜금리' 열을 시간 역순으로 정렬
df = df[::-1].reset_index(drop=True)
# 전월 대비 금리 변동 계산
df['날짜'] = pd.to_datetime(df['날짜'])
df['month'] = df['날짜'].dt.to_period('M')
monthly_mean_call_rate = df.groupby(df['month'])['콜금리'].mean()
monthly_mean_call_rate_series = pd.Series(monthly_mean_call_rate.values, index=monthly_mean_call_rate.index)
monthly_mean_call_rate_change_seriese = monthly_mean_call_rate_series.shift(1) - monthly_mean_call_rate_series
monthly_mean_call_rate_change_seriese = monthly_mean_call_rate_change_seriese.shift(-1)
monthly_df = pd.DataFrame({'month': monthly_mean_call_rate_change_seriese.index, 'monthly_mean_call_rate_change': monthly_mean_call_rate_change_seriese.values})
polar = []
for i in range(len(monthly_df.index)):
    if monthly_df['monthly_mean_call_rate_change'].iloc[i] > 0:
        polar.append(1)
    elif monthly_df['monthly_mean_call_rate_change'].iloc[i] < 0:
        polar.append(-1)
    else:
        polar.append(0)
monthly_df['polar'] = polar

# CSV 파일로 저장
monthly_df.to_csv("call_rate_label.csv", index=False)