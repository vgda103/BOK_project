# 다운로드
import re
import urllib.request
import pandas as pd
import os
import traceback

def pdf_downloader(csv_file_name):

    # CSV 파일을 불러와서 데이터프레임으로 변환
    df = pd.read_csv(csv_file_name, sep='\t')

    # 데이터프레임을 리스트 안의 튜플 데이터 형태로 변환
    total_info = [tuple(row) for row in df.values]

    dir = './reportpdf/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    for i in range(len(total_info)):
        try:
            pattern='\\d+\\.pdf'
            file_name = re.findall(pattern, total_info[i][0])
            file_name = total_info[i][1]+'_'+file_name[0]
            urllib.request.urlretrieve(total_info[i][0], dir+file_name)
        except:
            # print(f"{e}: {total_info[i][0]}")
            print(traceback.format_exc())
            i += 1 # 에러가 발생한 경우, 해당 항목부터 다시 크롤링할 수 있도록 i를 1 증가시킴
        if i%100==0:
            print(f'pdf {i}개 다운로드 완료') # 100개 다운로드마다 알림