from pathlib import Path

import scrapy
import csv
from einfomax_news.items import EinfomaxNewsItem
import re

class EinfoMaxSpider(scrapy.Spider):
    name = "einfomax"    
    
    def start_requests(self):
        total = 100 # 기사 건수
        pageNum = 20
        
        #for i in range(1, pageNum, 1):
        for i in range(1, pageNum):            
            yield scrapy.Request(
                f"https://news.einfomax.co.kr/news/articleList.html?page={i}&total={total}&box_idxno=&sc_area=A&view_type=sm&sc_word=%EA%B8%88%EB%A6%AC",
                self.parse_url)
    
    def parse_url(self, response):
        for sel in response.css('ul.type2'):
            # idx
            idx = sel.css('li > a::attr(href)').get()
            idx = re.sub(r'[^0-9]', '', idx)
            
            yield scrapy.Request(
                f"https://news.einfomax.co.kr/news/articleView.html?idxno={idx}",
                callback=self.parse_news)

    def parse_news(self, response):          
        item = EinfomaxNewsItem()
        
        # 기사 제목  
        item['title'] = response.css('#article-view > div > header > h3::text').get()
                        
        contents = response.css('#article-view-content-div > p::text').extract()[:-1]
        txt_list = ''
        for sel in contents:
            txt_list += sel
            
        article = txt_list.split(' = ')
        try:
            item['article'] = article[1]
        except:
            item['article'] = article[0]
        
        # 등록 일자
        w_date = response.xpath('//*[@id="article-view"]/div/header/div/article[1]/ul/li[2]/text()').get()
        item['w_date'] = w_date.replace('입력', '')
        
        print('*'*100)
        # print(item['title'])        
        # print(response.url)
        # print(article)
        # print(item['article'])        
                
        yield item