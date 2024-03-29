### BOK_project_TEAM2

### 텍스트 마이닝을 활용한 금융통화위원회 의사록 분석

1. 프로젝트 개요

Deciphering Monetary Policy Board Minutes with Text Mining 논문 분석 후 
2014년부터 2024까지의 금융통화위원회 의사록, 채권분석리포트, 이데일리, 연합 뉴스 기사 등 총 {}개의
자료 수집 후 전처리, 모델링 과정에서 감정 분석, 시각화를 통해 다음 금리 예측  

##### 프로젝트 기간

- 2024.03.21 ~ 2024-03-28

##### 진행 과정

1. 크롤링 프로그램 개발 (데이터 수집 - 한국은행 의사록 문서 / 채권분석 리포트 / 뉴스기사)
  
  - 데이터 수집(corpus 준비)
    - 기준 금리: https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643
      - corpus : 변경일자, 기준 금리

    - 한국은행 의사록(금융통화위원회:MPB, Monetary Policy Borad) : https://www.bok.or.kr/portal/bbs/B0000245/list.do?menuNo=200761
      - corpus : attach file(PDF)

    - 채권보고서 : https://finance.naver.com/research/debenture_list.naver
      - corpus : attach file(PDF)

    - 콜 금리(대한상공희의소) : https://www.korcham.net/nCham/Service/EconBrief/appl/ProspectBoardList.asp
      - corpus : 날짜, 콜금리, CD(91일), 국고채(3년), 국고채(5년), 회사채(3년, AA-)

    -  뉴스 기사
       -  corpus : 뉴스 기사(검색어 : 금리)
          - 이데일리 : https://www.edaily.co.kr/
          - 연합뉴스 : https://www.yna.co.kr/
          - 네이버 : https://news.naver.com/
       
2. 데이터 전처리(토큰화, 정규화 등) -> eknolpy 
   - Cleansing 
   - 토큰화
    - 명사(NNG), 형용사(VA, VAX), 부사(MAG), 동사(VA)만 사용
   - 정규화
     - 불용어 제거

3. 기능 선택
     - n-gram (n:1~5)

4. 모델링 → NBC or 사전기반분류(극성 분류)
   - 시장 접근 방식
     - NBC(Naive Bayes Classifier)
 
   - 평가 (★예정)
     - 수동으로 분류된 문장 테스트
     - 표본 외 테스트
 
5. 검증 (예측)
   - 감정 측정
     - n-gram의 특징을 통해 문장의 어조 측정
     - 문장의 어조로 문서의 어조를 측정

6. 시각화 (전체 문서에 대한 토큰 -> 워드클라우드 // 기준금리와 예측 자료 비교 그래프)

##### 개발 모듈
- edaily_crawl.py : 이데일리에서 금리로 검색한 기사 크롤링
- naver_crawl.py : 네이버 뉴스에서 금리로 검색한 기사 크롤링
- yna_crawl.py : 연합뉴스에서 금리로 검색한 기사 크롤링
- daily_call_rate_crawler.py
- adding_polar.py : 다음 월과의 콜금리 비교하여 상승한 경우 1, 하락한 경우 -1, 변화없는 경우 0으로 라벨링하여 년월 별 라벨링
- crawling_naver_report.py : 네이버 채권 분석 리포트 크롤링
- BOK_pdf.py : 의사록 크롤링
- report_cleanser.py : 네이버 채권 분석 리포트 크롤링 자료에 대한 클렌징
- bok_cleanser.py : 의사록 크롤링 자료에 대한 클렌징
- preprocessing : 클렌징된 자료에 대해 eKoNLPy 적용하여 토큰화
- ngram_add_label : 토큰화된 자료에 대해 ngram 형성하고, 해당 년월에 대한 라벨 추가 (adding_polar.py로부터 형성된 call_rate_label.csv 파일 사용)
- word_dict_maker.py : 형성된 ngram에 대해 단어 사전 구축
- polarity_calculator.py : ngram에 대해 극성 점수 계산
- date_classification.py : 금리 예측 및 실제값과 비교
- Bok_print.py : 시각화



##### 팀 주소(Notion)
https://www.notion.so/BOK-project-1e6d677f13e24e7e8041dd712c0fdfe2

##### 개발 기술 스택
1. 개발 환경
- Visual Studio Code
- GITHUB
- SLACK
- NOTION
- ONE DRIVE

2. 개발 언어 및 라이브러리
- 개발 언어
  - PYTHON
- 개발 라이브러리
  - PANDAS
  - eKoNLpy
  - SCRAPY