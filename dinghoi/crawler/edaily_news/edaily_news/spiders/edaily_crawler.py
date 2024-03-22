from pathlib import Path
#import csv
#import time

import scrapy
import re
from edaily_news.items import EdailyNewsItem

class EdailySpider(scrapy.Spider):
    name = "edaily"

    def start_requests(self):
        # url은 '금리'로 검색
        urls = []
        for i in range(1, 11):
        #for i in range(1, 501):
            urls.append(f"https://www.edaily.co.kr/search/news/?keyword=%ea%b8%88%eb%a6%ac&page={i}")
        
        for url in urls:            
            yield scrapy.Request(url=url, callback=self.parse_news)

    def parse_news(self, response):        
        item = EdailyNewsItem()
        for sel in response.css('.newsbox_04'):            
            # Index Number
            link = sel.css('a::attr(href)').get()            
            idx = link.split('&')            
            item['idx'] = re.sub(r'[^0-9]', '', idx[0])
            
            # 기사 제목
            item['title'] = sel.css('a > ul > li:nth-child(1)::text').get()
            
            # 기사 내용
            article = sel.xpath('a/ul/li[2]/text()').get()
            item['article'] = article.split(']')[1]
            
            # 언론사
            press = article.split(']')[0].replace('[', '')
            item['press'] = press.split(' ')[0]
            
            # 작성일
            item['w_date'] = sel.xpath('div/text()').get().strip()
            
            # print('*'*100)
            # print(item['w_date'])
            yield item
            
            