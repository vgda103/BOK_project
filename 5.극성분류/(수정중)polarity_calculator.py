# ngram까지 진행된 파일들을 대상으로 train:test=9:1로 split하여 극성 점수 계산
import os
import json
import pandas as pd
import random
import itertools
import numpy as np
# 반복 횟수 설정
num_iterations = 30
# 저장경로
dfdir = './dataframe/'
if not os.path.exists(dfdir):
    os.makedirs(dfdir)
json_folder = './ngram/'
doc_lists = os.listdir(json_folder)
for r in range(num_iterations):
    token_counts = {'-1': {}, '1': {}}
    random.shuffle(doc_lists)
    split_ratio = 0.9 # train:test = 9:1
    # train, test 데이터셋 분리
    split_index = int(len(doc_lists) * split_ratio)
    train_set = doc_lists[:split_index]
    test_set = doc_lists[split_index:]
    # train data의 경로
    train_file_path = [train for train in train_set]
    for file in train_file_path:
        with open(json_folder+file, encoding='utf-8')as f:
            data = json.load(f)
            label = data.get('label', None)
            if label is None: continue
            elif label == '1' or label == '-1':
                for i in range(1, 6):
                    grams = data.get(f'{i}gram', None)
                    if grams is None: continue
                    combined_grams = itertools.chain(*grams) # 리스트 내용물을 하나의 리스트로 통합 (중복있으므로 이를 카운팅하자!)
                    for gram in combined_grams:
                        token_counts[label][gram] = token_counts[label].get(gram, 0) + 1
    df = pd.DataFrame(token_counts) # 데이터프레임으로 만들기
    df.fillna(0, inplace=True) # NaN 값을 0으로 채우기
    df.index.name = 'ngram'
    # 데이터프레임의 각 열의 숫자를 더하여 총합을 구함
    column_sums = df.select_dtypes(include='number').sum()
    df.loc['Total'] = column_sums
    # 각 라벨에서 ngram이 등장할 확률(조건부확률) + LaplaceSmoothing
    k = 0.5
    df['P(ngram|1)'] = (df['1'] + k) / (df['1'].sum() + 2 * k)
    df['P(ngram|-1)'] = (df['-1'] + k) / (df['-1'].sum() + 2 * k)

    # 데이터프레임을 CSV 파일로 저장
    df.to_csv(dfdir + f'train{r+1}.csv')
    print(f'train{r+1}.csv 저장')

# 저장된 데이터프레임을 불러와서 극성 점수 평균내서 새로운 csv 파일로 저장