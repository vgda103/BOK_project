# 전체 문서에 대해 긍정/부정 비율을 통해 구축하였으며, 각 ngram은 15회 이상인 것들만 저장, 0으로 라벨링된 ngram이 없으므로 count는 -1과 1에 대해서만 진행

import os
import json
import pandas as pd

token_counts = {'-1': {}, '1': {}}
json_folder = './ngram/'
file_lists = [f for f in os.listdir(json_folder) if f.endswith('.json')] # 라벨링 완료된 json 파일 목록
for file in file_lists:
    with open(json_folder+file, encoding='utf-8') as f:
        data = json.load(f)
        label = data.get('label', None) # data['label']과 같은 결과이지만, 혹시 label이 없는 경우에 에러 발생하지 않고, None 반환하도록 함
        if label is None:
            continue
        
        for i in range(1, 6):
            grams = data.get(f'{i}gram', None)
            if grams is None:
                continue

            for gram_list in grams:
                if gram_list == []: # 문장의 단어 수가 부족한 경우 빈 리스트가 저장되기도 하므로, 빈리스트인 경우에는 pass
                    continue
                # print(gram_list)
                for gram in gram_list:
                    # gram = '_'.join(gram)
                    if gram not in token_counts[str(label)]: # 단어사전에 없는 경우 1
                        token_counts[label][gram] = 1
                    else: # 단어사전에 있는 경우 +1
                        token_counts[label][gram] += 1
    # break

df = pd.DataFrame(token_counts) # 데이터프레임으로 만들기

df['total'] = df.sum(axis=1) # ngram의 카운팅을 모두 더하기

df.fillna(0, inplace=True) # NaN 값을 0으로 채우기

df.index.name = 'ngram'
# df.to_csv('ngram_counts.csv')

# total이 15개 이상인 ngram만 남기기
df = df[df['total'] >= 15]
df.index.name = 'ngram'
# df.to_csv('ngram_counts_more_than_15.csv')

df['P/N'] = df['1'] / df['-1']
# 긍정/부정이 1.3 초과하면 '긍정', 1/1.3 미만이면 '부정', 그 외에는 'gray'로 표시
df['Sentiment'] = df['P/N'].apply(lambda x: 'P' if x > 1.3 else ('N' if x < 1/1.3 else 'gray'))

# 선택한 열만 저장
df_to_save = df['Sentiment']

# CSV 파일로 저장
df_to_save.to_csv('word_dict.csv')