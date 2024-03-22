# 크롤링 프로그램
from crawl1 import crawl_info
from crawl2 import pdf_downloader
from crawl3 import pdf_to_txt

csv_file_name = crawl_info() # csv 파일 이름 반환
pdf_downloader(csv_file_name) # pdf 파일 다운로드
pdf_to_txt(csv_file_name) # pdf 파일을 각각 txt 파일로 변환하여 저장