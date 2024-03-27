import scrapy
from news_crawl.items import NewsCrawlItem
# from pathlib import Path
import re
from datetime import datetime, timedelta
import pandas as pd
# import time

class EdailySpider(scrapy.Spider):
    name = "edaily"

    def start_requests(self):
        # start_date = '2024-01-01'
        # end_date = '2024-03-23'
        start_date = input('start (ex:2021-01-01): ')
        end_date = input('end (ex:2024-03-23): ')
        page_num = 500 # 크롤링할 페이징 개수(최대 500)

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
            if (s_date + timedelta(days=180)) <= e_date:
                edates = s_date + timedelta(days=180)                
            else:
                edates = e_date                
            end = edates.strftime('%Y-%m-%d').replace('-', '')
            
            # 페이징 Loop
            for i in range(1, total_page):
                url_param = f'/?source=total&keyword=금리&include=&exclude=&jname=&start={start}&end={end}&sort=latest&date=pick&exact=false&page={i}'

                # 콜백 함수 호출
                yield scrapy.Request(                    
                    url=f'https://www.edaily.co.kr/search/news'+url_param,
                    callback=self.parse_news
                    )
                
            s_date += timedelta(days=185) #6개월 단위 루프 설정

    def parse_news(self, response):
        item = NewsCrawlItem()
        for sel in response.css('.newsbox_04'):            
            # Index Number
            link = sel.css('a::attr(href)').get()            
            idx = link.split('&')            
            item['IDX'] = re.sub(r'[^0-9]', '', idx[0])

            try:
                csv = pd.read_csv('edaily.csv', encoding='utf-8')
                cnt = len(csv.loc[csv['IDX'] == int(item['IDX'])])

                if cnt > 0:
                    continue
            except:
                pass
            
            # 기사 제목
            item['TITLE'] = sel.css('a > ul > li:nth-child(1)::text').get()
            
            # 기사 내용
            # article = sel.xpath('a/ul/li[2]/text()').get()
            item['ARTICLE'] = sel.xpath('a/ul/li[2]/text()').get()    
     
            # 작성일
            item['WDATE'] = sel.xpath('div/text()').get().strip()

            item['URL'] = response.url

            print('*'*100)
            print(f"IDX: {item['IDX']} 진행 중...")           
            # print('#####', item['ARTICLE'])

            # time.sleep(0.5)
            yield item