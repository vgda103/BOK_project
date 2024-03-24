# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    IDX = scrapy.Field() # 인덱스 번호
    # PRESS = scrapy.Field() # 언론사
    TITLE = scrapy.Field() # 제목    
    ARTICLE = scrapy.Field() # 기사 내용        
    WDATE = scrapy.Field() # 등록일자
    URL = scrapy.Field()
    pass

from scrapy.exporters import CsvItemExporter

class HeadlessCsvItemExporter(CsvItemExporter):

    # def __init__(self, *args, **kwargs):
    #     kwargs['include_headers_line'] = False
    #     super(HeadlessCsvItemExporter, self).__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        # args[0] is (opened) file handler
        # if file is not empty then skip headers
        if args[0].tell() > 0:
            kwargs['include_headers_line'] = False

        super(HeadlessCsvItemExporter, self).__init__(*args, **kwargs)