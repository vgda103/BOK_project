import os
import pandas as pd
import kss
from ekonlpy.tag import Mecab

report_dir = './reporttxt/'
bok_dir = './Bok_txt/'
token_dir = './tokens/'

reportlist = [i for i in os.listdir(report_dir)]
bok_list = [i for i in os.listdir(bok_dir)]

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

# report tokenizing
for i in reportlist:
    if not os.path.exists(os.path.join(token_dir, i)):
        with open(report_dir+i, 'r', encoding='utf-8') as f:
            content = f.read()
            tokens = txt2filtered(content)

        with open(token_dir+i, 'w', encoding='utf-8') as f:
            f.write(str(tokens))
        f.close() 

# bok tokenizing
for i in bok_list:
    if not os.path.exists(os.path.join(token_dir, i)):
        with open(bok_dir+i, 'r', encoding='utf-8') as f:
            content = f.read()
            tokens = txt2filtered(content)
        
        with open(token_dir+i, 'w', encoding='utf-8') as f:
            f.write(str(tokens))
        f.close()
print('전처리 완료')