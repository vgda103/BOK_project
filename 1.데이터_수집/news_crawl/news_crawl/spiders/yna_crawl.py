import scrapy
from news_crawl.items import NewsCrawlItem
from pathlib import Path
import re
from datetime import datetime, timedelta
import pandas as pd
import json
# import time

class YnaSpider(scrapy.Spider):
    name = "yna"    
    
    def start_requests(self):        
        start_date = input('start (ex:2021-01-01): ')
        end_date = input('end (ex:2024-03-23): ')
        # start_date = '2024-03-20'
        # end_date = '2024-03-26'
        page_num = 50 # 크롤링할 페이징 개수(최대 50까지 가능)
        day = 30 # 날짜 Loop 일수

        url = 'https://ars.yna.co.kr/api/v2/search.asis'
        url_param = '?callback=Search.SearchPreCallback&query=%EA%B8%88%EB%A6%AC&period=diy'
        url_param += '&ctype=A&channel=basic_kr&page_size=10'
        target_url = url + url_param

        # 날짜 포멧
        s_date = datetime.strptime(start_date, '%Y-%m-%d')
        e_date = datetime.strptime(end_date, '%Y-%m-%d')

        total_page = int(page_num) + 1 # 루프 시 마지막 페이징 수 조정

        # 입력 일자 별 Loop
        while s_date <= e_date:
            # 시작 검색 일자 포멧
            sdates = s_date.strftime('%Y-%m-%d')
            start = sdates.replace('-', '')

            # 종료 검색 일자 포멧
            # edates = s_date + timedelta(days=180)
            if (s_date + timedelta(days=day)) <= e_date:
                edates = s_date + timedelta(days=day)                
            else:
                edates = e_date                
            end = edates.strftime('%Y-%m-%d').replace('-', '')            
            
            # 페이징 Loop
            for i in range(1, total_page):
                yield scrapy.Request(                    
                    url=target_url+f'&from={start}&to={end}&page_no={i}',
                    callback=self.parse_url
                    )
                                  
            s_date += timedelta(days=day)
    
    def parse_url(self, response):
        result_txt = response.text.split('Search.SearchPreCallback(')
        json_txt = result_txt[1][:-2]
        
        data = json.loads(json_txt)
    
        for sel in data['KR_ARTICLE']['result']:
            yield scrapy.Request(
                f"https://www.yna.co.kr/view/{sel['CONTENTS_ID']}?section=search",
                callback=self.parse_news
                )

    def parse_news(self, response):          
        item = NewsCrawlItem()
        write_yn = 1
       
        item['IDX'] = 'AKR' + re.sub(r'[^0-9]', '', response.url)      
       
        try:
            csv = pd.read_csv('yna.csv', encoding='utf-8')
            cnt = len(csv.loc[csv['IDX'] == int(item['IDX'])])

            if cnt > 0:
                write_yn = 0
        except:
            pass
        
        if write_yn == 1:   
            tag = response.xpath('//*[@id="articleWrap"]/div[2]/div/div/article').getall()
            clean_r = re.compile('<.*?>') # 정규표현식, 태그 제거
            clean_text = re.sub(clean_r, '', ''.join(tag)).strip()

            # print(clean_text)
            contents = clean_text.split('제보는')
            if contents[0]:
                item['ARTICLE'] = contents[0]

                # 기사 제목  
                item['TITLE'] = response.css('#articleWrap > div.content03 > header > h1::text').get()
                
                # 등록 일자
                wdate = response.xpath('//*[@id="newsUpdateTime01"]/text()').getall()
                
                item['WDATE'] = wdate[1]

                item['URL'] = response.url

                print('*'*100)
                print(f"IDX: {item['IDX']} 진행 중...")
                # print(item['ARTICLE'])
                
                yield item

