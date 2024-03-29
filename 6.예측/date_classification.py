import pandas as pd
import os
from ast import literal_eval
import re
from datetime import datetime
import numpy as np
from tqdm import tqdm

dictionary = pd.read_csv('./ngram_counts_more_than_15.csv')

dictionary['P/N'] = dictionary['1'] / dictionary['-1']
# 긍정/부정이 1.3 초과하면 '긍정', 1/1.3 미만이면 '부정', 그 외에는 'gray'로 표시
dictionary['Sentiment'] = dictionary['P/N'].apply(lambda x: 'P' if x > 1.3 else ('N' if x < 1/1.3 else 'gray'))
dictionary = dictionary[['ngram', 'Sentiment']]

df = pd.read_csv('./ngram.csv')
dates = []

for idx, row in df.iterrows():
    file_name = row['문서명']
    if '금융통화위원회' in file_name:
        date = re.findall(r'(?<=\()[0-9.].*?(?=\))', file_name)[1]
        date = date.strip(".")
        date = datetime.strptime(date, "%Y.%m.%d")
        date = date.strftime("%Y.%m.%d")
    elif 'edaily' in file_name:
        date = file_name.split('_')[1]
    else:
        date = file_name.split('_')[0]
        date = datetime.strptime(date, "%Y.%m.%d")
        date = date.strftime("%Y.%m.%d")

    dates.append(date)

df['date'] = dates

df = df[['date','토큰들리스트', 'label']]
df['doc_model_result'] = 'TBD'

print('datas are ready')

# 한 문서에 대하여 긍정/부정 라벨링

for idx, row in tqdm(df.iterrows()):
    doc = literal_eval(row['토큰들리스트'])

    p_sent_cnt = 0
    n_sent_cnt = 0

    for sent in doc:

        p_word_cnt = 0
        n_word_cnt = 0

        # 한 문장에 대하여 긍정/부정 라벨링
        
        for word in sent:
            try:
                if dictionary[dictionary['ngram'] == word]['Sentiment'].values[0] == 'P':
                    p_word_cnt += 1
                elif dictionary[dictionary['ngram'] == word]['Sentiment'].values[0] == 'N':
                    n_word_cnt += 1
            except:
                pass

        try: sent_tone = (p_word_cnt - n_word_cnt) / (p_word_cnt + n_word_cnt)
        except: pass
        
        
        if sent_tone > 0:
            p_sent_cnt += 1
        elif sent_tone < 0:
            n_sent_cnt += 1  

    try: doc_tone = (p_sent_cnt - n_sent_cnt) / (p_sent_cnt + n_sent_cnt)
    except: pass

    if doc_tone > 0:
        df.at[idx, 'doc_model_result'] = 1
    elif doc_tone < 0:
         df.at[idx, 'doc_model_result'] = -1
    else: df.at[idx, 'doc_model_result'] = 0

print('doc labelling completed')

# 날짜에 대하여 긍정/부정 라벨링

date_model_result = []

for i in tqdm(df['date'].unique()):
    try:
        p_doc_cnt = df[(df['date'] == i) & (df['doc_model_result'] == 1)].count()
        n_doc_cnt = df[(df['date'] == i) & (df['doc_model_result'] == -1)].count()
    except: pass

    if p_doc_cnt > n_doc_cnt:
        date_model_result.append(1)
    if p_doc_cnt < n_doc_cnt:
        date_model_result.append(-1)
    else: date_model_result.append(0)
    
date_and_model_result = pd.DataFrame({'date': df['date'].unique(), 'model_result':date_model_result})

print('date labelling completed')

# 실제 값과 비교

# 날짜 - 모델 결과
date_and_model_result = pd.DataFrame({'date': df['date'].unique(), 'model_result':date_model_result})
date_and_model_result['date'] = pd.to_datetime(date_and_model_result['date'])
date_and_model_result['month'] = date_and_model_result['date'].dt.to_period('M')

# 콜금리 변화 df
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

# ['date','month', 'polar', 'model_result'] 의 df 생성
k = pd.merge(date_and_model_result,monthly_df)
k = k[['date','month', 'polar', 'model_result']]

# 실제값과 예측값이 같은지 True/False 반환
polars = k['polar'].to_list()
results = k['model_result'].to_list()

k['comparison'] = [polar == result for polar, result in zip(polars, results)]

k.to_csv('./date_classification.csv')

print('file saved.\n프로그램을 종료합니다')