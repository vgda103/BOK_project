# 진짜최종최종최종

import os
import fitz
import pandas as pd
import kss
from ekonlpy.tag import Mecab
import re

def clean_str(text):
    text = re.sub('[-=+,#/\:^*\"※~&ㆍ』\\‘|\(\)\[\]\<\>`\'…》▲▼]','', string=text)
    pattern = '[^\w\s\n]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
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
    
def broker_filter(text, broker_name):
    if broker_name == '신한투자증권':
        pattern = '(Compliance Notice).*?(재배포될 수 없습니다.)'
        text = re.sub(pattern,'',string = text)
    elif broker_name == '한화투자증권':
        pattern = ['(Compliance Notice).*?(Licensee)','(Compliance Notice).*?(사용될 수 없습니다.)']
        for i in pattern:
            text = re.sub(i,'',string=text)
    elif broker_name == '교보증권':
        pattern = '(Compliance Notice).*?(얻으시기 바랍니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '하나증권':
        pattern = '(Compliance Notice).*?(사용될 수 없습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '키움증권':
        pattern = '(Compliance Notice).*?(책임을 지게 됩니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '이베스트증권':
        pattern = '(Compliance Notice).*?(관계에 있지 않습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '하이투자증권':
        pattern = '(Compliance notice).*?(주지하시기 바랍니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '메리츠증권':
        pattern = '(Compliance Notice).*?(배포 될 수 없습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == 'DS투자증권':
        pattern = '(Compliance Notice).*?(배포 할 수 없습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '이베스트투자증권':
        pattern = '(Compliance Notice).*?(관계에 있지 않습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '케이프투자증권':
        pattern = '(Compliance).*?(사용될 수 없습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '한국투자증권':
        pattern = '(본 자료는).*?(작성되었음을 확인합니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == 'DB금융투자':
        pattern = '(Compliance Notice).*?(기준으로 산출하였습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '현대차증권':
        pattern = '(Compliance Note).*?(사용될 수 없습니다.)'
        text = re.sub(pattern,'',string=text)
        pattern = '(본 조사자료는).*?(사용될 수 없습니다)'
        text = re.sub(pattern,'',string=text)
        pattern = '(본 조사지표는).*?(사용될 수 없습니다)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '대신증권':
        pattern = '(금융투자업규정).*?(Compliance Notice)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == 'LIG투자증권':
        pattern = '(Compliance).*?(사용될 수 없습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == 'KTB투자증권':
        pattern = '(www.ktb.co.kr).*?(변형할 수 없습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '이트레이드증권':
        pattern = '(Compliance Notice).*?(관계에 있지 않습니다.)'
        text = re.sub(pattern,'',string=text)
    elif broker_name == '메리츠종금증권':
        pattern = '(Compliance Notice).*?(판단으로 하시기 바랍니다.)'
        text = re.sub(pattern,'',string=text)
    return text
    

df = pd.read_csv("pdf_link_crawl_add_txt.csv", sep='\t')
# contents_list = []

pdf_dir = './reportpdf/'
txt_dir = './reporttxt/'

if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)

for i in df['file_name']:
    pdf_name = pdf_dir + i
    txt_name = txt_dir + df[df['file_name'] == i]['content_file']
    txt_name = txt_name.to_string(index = False)

    broker = df[df['file_name'] == i]['broker_name'].to_string(index=False)

    if broker == '미래에셋증권':
        pass
    else:
        # 파일이 이미 존재하는 경우에는 생성하지 않음
        if not os.path.exists(txt_name):
            with fitz.open(pdf_name) as doc:
                    contents = ''
                    for page in doc:
                        content = page.get_text()
                        content = content.replace('\n','blankblankblank')
                        contents += content

        sents = kss.split_sentences(contents)
        marked_sents = []
        for sent in sents:
            if 'blankblankblank blankblankblank' in sent:
                new_sent = sent.split('blankblankblank blankblankblank')
                marked_sents.extend(new_sent)
            else: 
                marked_sents.append(sent)

        unmarked_sents = [sent.replace('blankblankblank', '') for sent in marked_sents]
        unmarked_txt = broker_filter(''.join(unmarked_sents), broker_name=broker)
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
                

        with open(txt_name, 'w' , encoding='utf-8') as f:
            f.write(cleansed_txt)
