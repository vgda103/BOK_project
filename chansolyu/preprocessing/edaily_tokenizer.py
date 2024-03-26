import os
import pandas as pd
import kss
from ekonlpy.tag import Mecab
import re

token_dir = './tokens/'

if not os.path.exists(token_dir):
    os.makedirs(token_dir)

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

edaily_df = pd.read_csv('./news/edaily.csv')

for article in edaily_df['ARTICLE']:

    idx = edaily_df[edaily_df['ARTICLE'] == article]['IDX'].values[0]
    date = edaily_df[edaily_df['ARTICLE'] == article]['WDATE'].values[0]

    pattern = r'^.*?기자]'
    article = re.sub(pattern, '' , string=article)
    pattern = r'^.*?특파원]'
    article = re.sub(pattern, '' , string=article)
    email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    article = re.sub(email_pattern, '', string=article)
    url_pattern = r'(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    article = re.sub(url_pattern, '', string=article)
    no_meaning_pattern = r'([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음
    article = re.sub(no_meaning_pattern, '', string=article)

    tokens = txt2filtered(article)

    token_file_name = f"""edaily_{date}_{idx}.txt"""
    with open(token_dir+token_file_name, 'w') as f:
        f.write(str(tokens)) 