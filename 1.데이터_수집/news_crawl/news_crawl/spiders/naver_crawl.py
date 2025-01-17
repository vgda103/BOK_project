import scrapy
from news_crawl.items import NewsCrawlItem
from pathlib import Path
import re
from datetime import datetime, timedelta
import pandas as pd
import json
# import time
# import urllib

class NaverSpider(scrapy.Spider):
    name = "naver"

    def start_requests(self):
        press_list = ['1009', '1014', '1015'] # 언론사(매일경제:1009, 파이낸셜뉴스:1014, 한국경제:1015)
        s_date = input('start date(ex:2021-01-01): ') # 검색 시작 일자
        e_date = input('end date(ex:2024-03-24): ') # 검색 종료 일자

        # e_page = input('end page(ex:1 or 11 or 21 ...): ') # 검색 페이징 번호

        # press_list = ['1015']
        # s_date = '2024-03-24'
        # e_date = '2024-03-26'

        start = s_date.replace('-', '.')
        end = e_date.replace('-', '.')

        nso_sdate = s_date.replace('-', '')
        nso_edate = e_date.replace('-', '')
        
        day = 30 # 검색 루프 날짜 단위

        # 시작 url
        s_url = 'https://search.naver.com/search.naver'        
        
        # api url
        api_url = 'https://s.search.naver.com/p/newssearch/search.naver'

        for press in press_list:
            # 날짜 포멧
            s_fdate = datetime.strptime(s_date, '%Y-%m-%d')
            e_fdate = datetime.strptime(e_date, '%Y-%m-%d')

            # 입력 일자 별 Loop
            while s_fdate <= e_fdate:
                # 종료 검색 일자 포멧
                # edates = s_date + timedelta(days=180)
                if (s_fdate + timedelta(days=day)) <= e_fdate:
                    edates = s_fdate + timedelta(days=day)                
                else:
                    edates = e_fdate       

                end = edates.strftime('%Y-%m-%d').replace('-', '.')    
                nso_edate = edates.strftime('%Y-%m-%d').replace('-', '.')   

                for i in range(1, 500, 10):
                    if i == 1:
                        nso_sdate = s_date.replace('.', '')
                        nso_edate = e_date.replace('.', '')

                        s_param = '?where=news&query=%EA%B8%88%EB%A6%AC'
                        s_param += '&sm=tab_opt&sort=0&photo=0&field=0&pd=0'
                        s_param += '&ds=&de=&docid=&related=0&mynews=1'
                        s_param += '&office_type=1&office_section_code=3&nso=&is_sug_officeid=0'
                        s_param += '&office_category=0&service_area=0'
                        s_param += f'&news_office_checked={press}'
                        s_param += f'&de={end}&ds={start}'
                        s_param += f'nso=so%3Ar%2Cp%3Afrom{nso_sdate}to{nso_edate}'
                        target_url = s_url + s_param
                    
                        yield scrapy.Request(
                            url=target_url,           
                            callback=self.parse_url,               
                            )
                    else:
                        nso_sdate = start.replace('.', '')
                        nso_edate = end.replace('.', '')                    
                        
                        api_param = f'?eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=1'
                        api_param += '&nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22finance%22%7D%7D%7D'
                        api_param += '&nso=%26nso%3Dso%3Ar%2Cp%3Afrom20210101to20240324%2Ca%3Aall&nx_and_query=&nx_search_hlquery='
                        api_param += '&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=3&office_type=1&pd=3&photo=0'
                        api_param += '&query=%EA%B8%88%EB%A6%AC&query_original=&service_area=0&sort=0&spq=0&where=news_tab_api'
                        api_param += f'&cluster_rank={i+1}'
                        api_param += f'&de={end}&ds={start}'
                        api_param += f'&news_office_checked={press}'
                        api_param += f'&start={i}'
                        api_param += f'&nso=so:r,p:from{nso_sdate}to{nso_edate},a:all'
                        target_url = api_url + api_param

                        # print(target_url)

                        yield scrapy.Request(
                                url=target_url,           
                                callback=self.parse_json,               
                                )
                s_fdate += timedelta(days=day)

    def parse_url(self, response):
        news_cnt = len(response.css('.bx').getall())

        for i in range(1, news_cnt): 
            # news 기사 url
            a_url = response.css(f'#sp_nws{i} > div > div > div.news_contents > a.news_tit::attr(href)').get()

            if a_url is None: # 없을 경우 건너뛰기
                continue
           
            yield scrapy.Request(
                url=a_url,
                callback=self.parse_news
            )            
    
    def parse_json(self, response):
        data = json.loads(response.text)
        news_cnt = len(data['contents'])

        # print('next1', data['nextUrl'])

        if news_cnt > 0:
            for i in range(1, news_cnt+1):
                a_url = re.findall(
                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
                    data['contents'][i-1]
                    )
                
                # print(a_url)
                
                if a_url is None: # 없을 경우 건너뛰기
                    continue

                yield scrapy.Request(
                    url=a_url[0],
                    callback=self.parse_news
                )

        # if data['nextUrl']:
        #     yield scrapy.Request(
        #         url=data['nextUrl'],
        #         callback=self.parse_next,
        #         meta={'next_url':data['nextUrl']}
        #     )

    # def parse_next(self, response):
    #     next_url = response.meta['next_url']

    #     print('next2', next_url)

    #     yield scrapy.Request(
    #         url=next_url,
    #         callback=self.parse_json
    #     )

    def parse_news(self, response):  
        item = NewsCrawlItem()
        write_yn = 1 # 중복체크 기본값

        # print('news')

        item['URL'] = response.url
        item['IDX'] = re.sub(r'[^0-9]', '', item['URL'])

        # print(item['IDX'])

        # 중복 체크
        try:
            csv = pd.read_csv('naver.csv', encoding='utf-8')
            cnt = len(csv.loc[csv['IDX'] == int(item['IDX'])])

            if cnt > 0:
                write_yn = 0
                print('*'*100)
                print('duplicate index number.')
        except:
            pass

        if write_yn == 1:
            clean_r = re.compile('<.*?>') # 정규표현식, 태그 제거

            if item['URL'].count('fnnews') > 0: # 파이낸셜 : 1014
                item['TITLE'] = response.css('#fn_wrap > div > div.inner_box.view > div.wrap_view_hd > h1::text').get()

                tag = response.xpath('//*[@id="article_content"]').getall()         
                article = re.sub(clean_r, '', ''.join(tag)).strip()
                article = article.split('function')
                article = article[0].split('fn_getContentDate')
                item['ARTICLE'] = article[0]

                item['WDATE'] = response.css('#fn_wrap > div > div.inner_box.view > div.wrap_view_hd > div > div.info > span.row-2 > p:nth-child(2)::text').get()
            elif item['URL'].count('hankyung') > 0: #한국경제 : 1015
                item['TITLE'] = response.css('#container > div > div > article > h1::text').get()

                tag = response.xpath('//*[@id="articletxt"]').getall()
                article = re.sub(clean_r, '', ''.join(tag)).strip()
                article = article.split('function')
                article = article[0].split('fn_getContentDate')
                item['ARTICLE'] = article[0]

                item['WDATE'] = response.css('#container > div > div > article > div > div > div.article-timestamp > div.datetime > span:nth-child(1) > span::text').get()
            else: # 매일경제 : 1009
                item['TITLE'] = response.css('#container > section > div.news_detail_head_group.type_none_bg > section > div > div > div > h2::text').get()

                tag = response.xpath('//*[@id="container"]/section/div[3]/section/div[1]/div[1]/div[1]').getall()
                
                article = re.sub(clean_r, '', ''.join(tag)).strip()
                article = article.split('function')
                article = article[0].split('fn_getContentDate')
                item['ARTICLE'] = article[0]

                item['WDATE'] = response.css('#container > section > div.news_detail_body_group > section > div.min_inner > header > div > div.news_write_info_group > div > div > dl > dd::text').get()
            
            print('*'*100)
            print(f"IDX: {item['IDX']} 진행 중...")
            # print(item['ARTICLE'])

            yield item
