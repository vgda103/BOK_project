from pathlib import Path

import scrapy
import csv

class InfoMaxSpider(scrapy.Spider):
    name = "infomax"    
    
    def start_requests(self):
        f = open('../assets/infomax_idx.csv', 'r', encoding='utf-8')
        csv_reader = csv.reader(f)
        next(csv_reader) # 첫째행 제외(column 명)
        
        # '금리' 검색 url        
        for line in csv_reader:
            url = f"https://news.einfomax.co.kr/news/articleView.html?idxno={line[0]}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):  
        item = {}              
        # 기사 제목  
        item['title'] = response.css('#article-view > div > header > h3::text').get()        
        
        # 언론사
        item['press'] = '연합인포맥스'
        
        # 기자
        item['reporter'] = response.css('#anchorTop > article.writer > div:nth-child(1) > div > strong::text').get()
        
        # # 등록 일자
        write_date = response.xpath('//*[@id="article-view"]/div/header/div/article[1]/ul/li[2]/text()').get()
        item['write_date'] = write_date.replace('입력', '')
        
        text_lists = response.xpath('//*[@id="article-view-content-div"]/p[1]/text()').get()
        
        article = ''                
        for list in text_lists:
            article += list
        item['article'] = article
            
        #print(f'title:{title}, article:{article}, press:{press}, reporter:{reporter}, write_date:{write_date}')
        yield item
    # print('진행 완료!!!')
        
            