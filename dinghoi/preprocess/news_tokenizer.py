import os
import pandas as pd
import kss
from ekonlpy.tag import Mecab
import re
# import itertools
import time


token_dir = './tokens/'

if not os.path.exists(token_dir):
    os.makedirs(token_dir)

def clean_text(text):
    pattern = r'^.*?기자]'
    text = re.sub(pattern, '' , string=text)
    pattern = r'^.*?특파원]'
    text = re.sub(pattern, '' , string=text)
    email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    text = re.sub(email_pattern, '', string=text)
    url_pattern = r'(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    text = re.sub(url_pattern, '', string=text)
    no_meaning_pattern = r'([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음
    text = re.sub(no_meaning_pattern, '', string=text)
    
    return text

def txt2filtered(self):
    sents = kss.split_sentences(self)
    sents = [sent.replace('\n','') for sent in sents]
    all_filtered_tokens = []
    for sent in sents:
        tokenizer = Mecab()
        tokens = tokenizer.pos(sent)
        filtered_tokens = []
        for token in tokens:
            if token[1] in ['NNG', 'VA', 'VAX','MAG','VA']:
                filtered_tokens.append(token[0])
        all_filtered_tokens.append(filtered_tokens)
    return all_filtered_tokens

news_list = {      
    'yna_crawl.csv' : 'yna',    
    'naver_crawl.csv' : 'naver',
    # 'edaily_crawl.csv' : 'edaily',      
}

file_path = './news/'

for key, value in news_list.items():
    file_path = f'./news/{key}'
    news_df = pd.read_csv(file_path, encoding='utf-8')

    for article in news_df['ARTICLE']:
        try:
            idx = news_df[news_df['ARTICLE'] == article]['IDX'].values[0]
            date = news_df[news_df['ARTICLE'] == article]['WDATE'].values[0]

            date_str = date.split(' ')
            f_date = date_str[0].replace('-', '.')

            token_file_name = f"""{value}_{f_date}_{idx}.txt"""

            if os.path.isfile(token_dir+token_file_name): # 중복 파일 건너뛰기 
                print('duplicate file...')  
                continue
            
            article = clean_text(article)

            tokens = txt2filtered(article)

            with open(token_dir+token_file_name, 'w', encoding='utf-8') as f:
                f.write(str(tokens)) 
        
            # print('*'*100)
            print(f'{value}:{idx} 진행 중...')
        except:
            # print('*'*100)
            print('Error!!!')
            continue
        time.sleep(0.1)        