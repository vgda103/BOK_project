import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 날짜,제목 및 pdf url 크롤링하여 csv 파일로 저장
def crawl_info():
    total_info = []
    for k in range(1, 90):
        page = k
        URL = f'https://finance.naver.com/research/debenture_list.naver?keyword=&brokerCode=&searchType=writeDate&writeFromDate=2021-01-01&writeToDate=2023-12-31&x=40&y=21&page={page}'
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_tags = soup.select('tr')
        info = []
        for table_tag in table_tags:
            try:
                title_tag = table_tag.select_one('td > a')
                pdf_tags = table_tag.select('td.file > a')
                date_tags = table_tag.select('td.date')
                if pdf_tags!=[] and date_tags!=[]:
                    pdf = pdf_tags[0].attrs['href']
                    date = date_tags[0].text
                    title = title_tag.text
                    pattern='\\d+\\.pdf'
                    file_name = re.findall(pattern, pdf)
                    file_name = date+'_'+file_name[0]
                    info.append((pdf, date, title, file_name))
            except:
                title_tag = table_tag.select_one('td > a')
                print(f'error {title_tag.text}')
        total_info.extend(info)

    # 데이터프레임으로 변환
    df = pd.DataFrame(total_info, columns=["pdf_link", "date", "title", "file_name"])
    df['content_file'] = df['file_name'].apply(lambda x : x.replace('.pdf', '.txt'))

    # 데이터프레임을 CSV 파일로 저장
    df.to_csv("pdf_link_crawl_add_txt.csv", sep='\t', index=False)
    return 'pdf_link_crawl_add_txt.csv'