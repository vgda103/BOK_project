import os
import fitz
import pandas as pd
import kss
from ekonlpy.tag import Mecab
import re

def clean_str(text):
    text = re.sub('[-=+,#/\:^*\"※~&ㆍ』\\‘|\(\)\[\]\<\>`\'…》▲▼]','', string=text)
    return text 

def contains_patterns(text):
    email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    url_pattern = r'(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    no_meaning_pattern = r'([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음

    # 각 패턴에 대한 검사
    contains_email = bool(re.search(email_pattern, text))
    contains_url = bool(re.search(url_pattern, text))
    contains_no_meaning = bool(re.search(no_meaning_pattern, text))

    # 어떤 패턴이라도 하나라도 포함되어 있는지 여부를 반환
    return contains_email or contains_url or contains_no_meaning



def is_meaningful(sentence):
    if len(sentence.split()) > 4:
        return True
    else: 
        return False
    
def filter_contents(text):
    pattern = r'^.*?다음과 같은 토의가 있었음.'
    text = re.sub(pattern, '' , string=text)
    pattern = r'^.*?위원 토의내용'
    text = re.sub(pattern, '' , string=text)
    return text
    

pdf_dir = './Bok_pdf/'
txt_dir = './Bok_txt/'
    
pdf_list = [i for i in os.listdir(pdf_dir) if '.pdf' in i]

# index_df 불러오기
with open(pdf_dir+'index.txt', 'r') as f:
    df = []
    for row in f.readlines():
        row = row.strip().split('\t')
        df.append(row)
    df = pd.DataFrame(df, columns= ['date','pdf_name', 'txt_name'])

if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)

for i in pdf_list:
    txt_name = txt_dir + df[df['pdf_name']==i]['txt_name'].to_string(index=False)

    # 파일이 이미 존재하는 경우에는 생성하지 않음
    if not os.path.exists(txt_name):
        with fitz.open(pdf_dir+i) as doc:
            contents = ''
            for page in doc:
                content = page.get_text()
                content = content.replace('\n','blankblankblank')
                contents += content
                contents = re.sub('(-).*?[\d].*?(-)','',contents ) # 페이지 표시 제거

    sents = kss.split_sentences(contents)
    marked_sents = []
    for sent in sents:
        if 'blankblankblank blankblankblank' in sent:
            new_sent = sent.split('blankblankblank blankblankblank')
            marked_sents.extend(new_sent)
        else: 
            marked_sents.append(sent)

    unmarked_sents = [sent.replace('blankblankblank', '') for sent in marked_sents]
    unmarked_txt = filter_contents(''.join(unmarked_sents))
    final_sents = kss.split_sentences(unmarked_txt)

    cleansed_txt = ''
    cleansed_sents = []
    for sent in final_sents:
        sent = clean_str(sent)
        if contains_patterns(sent) == False and is_meaningful(sent):
            if cleansed_sents.count(sent) > 3:
                pass
            else:
                cleansed_sents.append(sent)
                cleansed_txt += sent   

    with open(txt_dir+i.replace('.pdf','.txt'), 'w' , encoding='utf-8') as f:
            f.write(cleansed_txt)