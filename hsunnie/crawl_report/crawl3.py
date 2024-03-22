# csv 파일 열어서 df로 만든 뒤, 각 pdf 파일을 text 파일로 변환하여 저장
import pandas as pd
import fitz
import os

def pdf_to_txt(csv_file_name):
    # CSV 파일을 불러와서 데이터프레임으로 변환
    df = pd.read_csv(csv_file_name, sep='\t')

    dir = './reportpdf/'
    dir2 = './reporttxt/'
    if not os.path.exists(dir2):
        os.makedirs(dir2)
    content = ''
    for i in range(len(df)):
        df_info_list = df.iloc[i].to_list()
        pdf_name = dir + df_info_list[3]
        with fitz.open(pdf_name) as doc:
            for page in doc:
                content += page.get_text()
                txt_name = dir2 + df_info_list[4]
                with open(txt_name, 'w', encoding='utf-8') as f:
                    f.write(content)
        if i%100==0:
            print(f'txt {i}개 변환 완료') # 100개 변환마다 알림
    return '모든 pdf 파일에 대해 txt 파일로 변환 완료'