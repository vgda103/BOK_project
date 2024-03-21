from pathlib import Path

import scrapy
import re

class EdailySpider(scrapy.Spider):
    name = "edaily"

    def start_requests(self):
        # '금리' 검색 url        
        urls = []
        for i in range(1, 11):
        #for i in range(1, 501):
            urls.append(f"https://www.edaily.co.kr/search/news/?keyword=%ea%b8%88%eb%a6%ac&page={i}")
        
        for url in urls:            
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news_lists = response.css('.newsbox_04')
        item = {}                        
        for news_list in news_lists:
            # Index Number
            link = news_list.css('a::attr(href)').get()            
            idx = link.split('&')            
            item['idx'] = re.sub(r'[^0-9]', '', idx[0])
            
            # 기사 제목
            item['title'] = news_list.css('a > ul > li:nth-child(1)::text').get()
            
            contents = news_list.xpath('a/ul/li[2]/text()').get()
            splt = contents.split(']')[0].replace('[', '')
            
            item['article'] = contents.split(']')[1] # 기사 내용            
            
            item['press'] = splt.split(' ')[0] # 언론명
            item['reporter'] = splt.split(' ')[1] # 기자명
            
            item['write_date'] = news_list.xpath('div/text()').get().strip() # 기사 작성일
            
            #print(f'idx:{idx}, title:{title}, article:{article}, press:{press}, reporter:{reporter}')
            yield item
        print('진행 완료!!!')
            
            