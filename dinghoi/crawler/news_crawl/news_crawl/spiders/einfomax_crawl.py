import scrapy
from news_crawl.items import NewsCrawlItem
from pathlib import Path
import re
from datetime import datetime, timedelta
import pandas as pd
# import time

class EinfoMaxSpider(scrapy.Spider):
    name = "einfomax"    
    
    def start_requests(self):
        s_page = input('start number(paging) :')
        e_page = input('end number(2021년 기준:3000) :')
        news_total = 300000 # 기사 건수

        total_page = int(e_page) + 1
        for i in range(int(s_page), total_page):            
            yield scrapy.Request(
                url=f"https://news.einfomax.co.kr/news/articleList.html?page={i}&total={news_total}&box_idxno=&sc_area=A&view_type=sm&sc_word=%EA%B8%88%EB%A6%AC",
                callback=self.parse_url)
    
    def parse_url(self, response):
        for i in range(1, 21):
            # idx
            idx_no = response.css(f'#section-list > ul > li:nth-child({i}) > a::attr(href)').get()
            if idx_no is None:
                idx_no = response.css(f'#section-list > ul > li:nth-child({i}) > h4 > a::attr(href)').get()
            idxno = re.sub(r'[^0-9]', '', idx_no)

            # print(i, idx_no)
           
            yield scrapy.Request(
                f"https://news.einfomax.co.kr/news/articleView.html?idxno={idxno}",
                callback=self.parse_news)

    def parse_news(self, response):          
        item = NewsCrawlItem()
        write_yn = 1
        
        item['IDX'] = re.sub(r'[^0-9]', '', response.url)        
        # f_path = Path('einfomax.csv')
        # if f_path.is_file():
        try:
            csv = pd.read_csv('einfomax.csv', encoding='utf-8')
            cnt = len(csv.loc[csv['IDX'] == int(item['IDX'])])

            if cnt > 0:
                write_yn = 0
        except:
            pass
        
        if write_yn == 1:   
            # txt_list = response.css('#article-view-content-div > p::text').extract()[:-1]
            # contents = ''
            # for sel in txt_list:
            #     contents += sel 

            tag = response.xpath('//*[@id="article-view-content-div"]').getall()
            clean_r = re.compile('<.*?>') # 정규표현식, 태그 제거
            clean_text = re.sub(clean_r, '', ''.join(tag)).strip()
            contents = clean_text.split('(끝)')
            if contents[0]:
                item['ARTICLE'] = contents[0]

                # 기사 제목  
                item['TITLE'] = response.css('#article-view > div > header > h3::text').get()
                
                # 등록 일자
                w_date = response.xpath('//*[@id="article-view"]/div/header/div/article[1]/ul/li[2]/text()').get()
                item['WDATE'] = w_date.replace('입력', '')

                item['URL'] = response.url

                print('*'*100)
                print(f"IDX: {item['IDX']} 진행 중...")
                # print(contents)
                # tag = response.xpath('//*[@id="article-view-content-div"]').getall()
                # cleanr = re.compile('<.*?>')
                # cleantext = re.sub(cleanr, '', tag[0])
                # print(cleantext)
                
                yield item