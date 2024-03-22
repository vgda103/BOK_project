# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EdailyNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    idx = scrapy.Field() # 인덱스 번호
    title = scrapy.Field() # 제목    
    article = scrapy.Field() # 기사 내용
    press = scrapy.Field() # 언론사    
    w_date = scrapy.Field() # 등록일자
    pass
