from pathlib import Path

import scrapy
import re

class InfomaxIdxSpider(scrapy.Spider):
    name = "infomax_idx"    
            
    def start_requests(self):        
        urls = []
        for i in range(1, 11):        
            urls.append(f"https://news.einfomax.co.kr/news/articleList.html?page={i}&total=200280&box_idxno=&sc_area=A&view_type=sm&sc_word=%EA%B8%88%EB%A6%AC")
            
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news_lists = response.css('ul.type2')
        item = {}                        
        for news_list in news_lists:
            # idx
            link = news_list.css('li > a::attr(href)').get()
            item['idx'] = re.sub(r'[^0-9]', '', link)
            
            #print(f'idx:{idx}')
            yield item
        print('진행 완료!!!')