from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import random
import numpy as np

def open_file( path ) -> str:
    """
    파일열기 반환은 str
    path : 파일경로, 파일이름 까지
    """

    # 예외 처리문
    try:
        # 파일 열기 
        with open( path, 'r' ) as txt_f:
            return txt_f.read()
    # 파일을 못찾았을 경우 에러 처리
    except FileNotFoundError:
        print(f"File { path } not found.")
    # 예상치 못한 에러를 처리 하는 곳
    except Exception as e:
        print(f"An error occurred while processing { path }: {e}")
    # 정상 작동시 처리되는 곳
    # else:
    #     print( 'txt 변환' )
        pass
    return 
    pass # open_file 끝

class Bok_print:

    def __init__(self) -> None:
        plt.rcParams['font.family'] = 'Malgun Gothic'
        pass # __init__ 끝
    

    def Bok_coll( self ):

        str_data = open_file( 'daily_call_rate.csv' )
        str_data = str_data.split( '\n' )
        str_data = str_data[ 1: ]

        test_data = {} # 

        calls_base = {} # 원본값

        for str_in in str_data:

            if str_in == '':
                continue
            
            temp = str_in.split( ',' )
            
            calls_base[ temp[ 0 ] ] = float( temp[ 1 ] )
            test_data[ temp[ 0 ] ] = round(random.uniform(1.50, 3.50), 2)
            pass # for str_in 끝

        # print( calls_base )

        coll_dates = [ datetime.strptime( date, '%Y.%m.%d' ) for date in calls_base.keys() ]
        coll_values = list( calls_base.values() )
        
        pred_dates = [ datetime.strptime( date, '%Y.%m.%d' ) for date in test_data.keys() ]
        pred_values = list( test_data.values() )

        plt.figure( figsize=( 20, 8 ) )
        plt.plot( coll_dates, coll_values, label='원본 데이터' )
        plt.plot( pred_dates, pred_values, color='red', linestyle='--', label='테스트 데이터' )

        plt.xlabel( '금리' )
        plt.ylabel( '날자' )
        plt.title( '콜금리와 예측 금리' )
        plt.xticks( rotation=45 )
        plt.grid( True )
        plt.tight_layout()
        plt.show()
        
        pass # Bok_coll 끝

    def out_wordcloud( self, text, width=8, height=8, back_color='white' ) -> None:
        """
        워드클라우드로 출력
        text : 문자열
        width : 출력 너비, 기본값은 8, plt.figurer 에서 조절함
        hight : 출력 높이, 기본값은 8, plt.figurer 에서 조절함
        back_color : 배경컬러, 기본값 white
        """
        # 워드클라우드 객체 생성및 폰트, 배경색 설정
        wordcloud = WordCloud( font_path='C:/Windows/Fonts/malgun.ttf',
                            background_color=back_color )
        # 출력할 텍스트 입력
        wordcloud.generate( text )

        # 출력할 너비와 높이 설정
        plt.figure( figsize=( width, height ) )
        # 워드클라우드가 이미지 타입이라 이미지 출력 설정,
        # interpolation은 옵션설정이면 bilinear은 보간 방법으로 설정
        plt.imshow( wordcloud, interpolation='bilinear' )
        # 눈금 비활성화
        plt.axis( 'off' )
        # 출력
        plt.show()

        pass # out_wordcloud 끝
    
    def img_out_wordcloud( self, path, text, width=8, height=8, back_color='white' ) -> None:
        """
        워드클라우드로 형태로 출력
        path : 그림파일 형식의 이미지 경로
        text : 문자열
        width : 출력 너비, 기본값은 8, plt.figurer 에서 조절함
        hight : 출력 높이, 기본값은 8, plt.figurer 에서 조절함
        back_color : 배경컬러, 기본값 white
        """
        mask_image = np.array( Image.open( path ) )

        wordcloud = WordCloud( font_path='C:/Windows/Fonts/malgun.ttf',
                    mask=mask_image, background_color=back_color ).generate( text )
        
        plt.figure( figsize=( width, height ) )
        plt.imshow( wordcloud, interpolation='bilinear' )
        plt.axis( 'off' )
        plt.show()
        pass # img_out_wordcloud 끝


    pass # Bok_print 끝

a = Bok_print()
a.Bok_coll()
# 텍스트 데이터 준비
text = "파이썬은 인공지능 및 데이터 분석에서 널리 사용되고 있습니다. 파이썬을 배우는 것은 재미있고 유용한 경험이 될 것입니다."
a.out_wordcloud( text )
a.img_out_wordcloud( './istockphoto.jpg', text )