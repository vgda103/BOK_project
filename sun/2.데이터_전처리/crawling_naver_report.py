import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import urllib.request
import os
import traceback

# 데이터 정보 크롤링 (pdf 링크 / 날짜 / 제목 / 증권사이름 / pdf 파일이름 / txt 파일이름)
def crawl_info():
    total_info = []
    page = 1  # 페이지 초기값 설정
    while True:
        URL = f'https://finance.naver.com/research/debenture_list.naver?keyword=&brokerCode=&searchType=writeDate&writeFromDate=2014-01-01&writeToDate=2023-12-31&x=46&y=21&page={page}'
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_tags = soup.select('tr')
        info = []
        for table_tag in table_tags:
            try:
                td_tags = table_tag.select('td')
                if len(td_tags) >= 2:
                    title_tag = td_tags[0].select_one('a')
                    pdf_tags = table_tag.select('td.file > a')
                    date_tags = table_tag.select('td.date')
                    broker_name = td_tags[1].text.strip()
                    if pdf_tags and date_tags:
                        pdf = pdf_tags[0].attrs['href']
                        date = '20' + date_tags[0].text
                        title = title_tag.text
                        pattern = '\\d+\\.pdf'
                        file_name = re.findall(pattern, pdf)
                        file_name = date + '_' + file_name[0]
                        info.append((pdf, date, title, broker_name, file_name))
            except Exception as e:
                print(f'Error: {e}')
        total_info.extend(info)
        
        # "맨뒤" 버튼이 없을 경우 탐색을 멈춤
        last_button = soup.select_one('td.pgRR > a')
        if not last_button:
            break
        page += 1  # 다음 페이지로 이동

    # 데이터프레임으로 변환
    df = pd.DataFrame(total_info, columns=["pdf_link", "date", "title", "broker_name", "file_name"])
    df['content_file'] = df['file_name'].apply(lambda x: x.replace('.pdf', '.txt'))

    # 데이터프레임을 CSV 파일로 저장
    df.to_csv("pdf_link_crawl_add_txt.csv", sep='\t', index=False)
    return 'pdf_link_crawl_add_txt.csv'

# pdf download
def pdf_downloader(csv_file_name):
    df = pd.read_csv(csv_file_name, sep='\t') # CSV 파일을 데이터프레임으로 변환
    total_info = [tuple(row) for row in df.values] # 데이터프레임을 리스트 안의 튜플 데이터 형태로 변환

    dir = './reportpdf/' # pdf 파일 저장할 경로 설정
    if not os.path.exists(dir): # 폴더 없는 경우에 생성하는 코드
        os.makedirs(dir)

    for i in range(len(total_info)):
        if i==0:
            print('pdf 다운로드 시작')
        try:
            pattern='\\d+\\.pdf'
            file_name = re.findall(pattern, total_info[i][0])
            file_name = total_info[i][1]+'_'+file_name[0]
            urllib.request.urlretrieve(total_info[i][0], dir+file_name)
        except:
            print(f"error : {total_info[i][0]}")
            print(traceback.format_exc())
            i += 1 # 에러가 발생한 경우, 해당 항목부터 다시 크롤링할 수 있도록 i를 1 증가시킴
        if i!=0 and i%100==0:
            print(f'pdf 다운로드 진행률 : {i}/{len(total_info)}') # 100개 다운로드마다 알림

# 함수 실행 (크롤링 & csv 파일 저장 -> pdf 저장)
pdf_downloader(crawl_info())