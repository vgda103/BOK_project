from pathlib import Path

import scrapy
import csv
from naver_news.items import NaverNewsItem
import re

import urllib

class EinfoMaxSpider(scrapy.Spider):
    name = "naver"    
    
    def start_requests(self):
        url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&ssc=tab.news.all&query=%EA%B8%88%EB%A6%AC&oquery=%EA%B8%88%EB%A6%AC&tqi=iQ0%2BnlqVN8wsscgh%2F5Csssssteh-360332&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=0&office_section_code=0&office_type=0&pd=0&photo=0&sort=0'
        
        yield scrapy.Request(
            url=url,
            callback=self.parse_url
            )
        
        # yield scrapy.Request(
        #     url='https://s.search.naver.com/p/newssearch/search.naver?cluster_rank=55&de=&ds=&eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=0&news_office_checked=&nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22finance%22%7D%7D%7D&nso=%26nso%3Dso%3Ar%2Cp%3Aall%2Ca%3Aall&nx_and_query=&nx_search_hlquery=&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=0&office_type=0&pd=0&photo=0&query=%EA%B8%88%EB%A6%AC&query_original=&service_area=0&sort=0&spq=2&start=21&where=news_tab_api&nso=so:r,p:all,a:all&_callback=jQuery1124016267946258576105_1711095359545&_=1711095359547',
        #     # formdata=params,
        #     callback=self.parse_url,
        #     # method='POST',            
        #     )
    
    def parse_url(self, response):
        params = {
            'cluster_rank' : '222',
            'de' : '',
            'ds' : '',
            'eid' : '',
            'field' : '0',
            
            
            'is_dts' : '0',
            'is_sug_officeid' : '0',
            'mynews' : '0',            
            'nqx_theme' : '{"theme":{"main":{"name":"finance"}}}',
            'nso' : '&nso=so:r,p:all,a:all',
            'office_category' : '0',
            'office_section_code' : '0',
            'office_type' : '0',
            'pd' : '0',
            'photo' : '0',
            'query' : '금리',
            'service_area' : '0',
            'sort' : '0',
            'spq' : '2',
            'start' : '121',
            'where' : 'news_tab_api',
            'nso' : 'so:r,p:all,a:all',
            '_callbak' : 'jQuery112406313420679743547_1711092744067',
            '_' : '1711092744079'
        }
        
        yield scrapy.FormRequest(
            url='https://s.search.naver.com/p/newssearch/search.naver',
            formdata=params,
            callback=self.parse_news,
            method='POST',            
            )
        
    def parse_news(self, response):          
        item = NaverNewsItem()
        
        print('*'*100)
        #print(response.css('#sp_nws222 > div.news_wrap.api_ani_send > div > div.news_contents > a.news_tit::attr(href)').get())        
        print(response.text)
       
        #yield item