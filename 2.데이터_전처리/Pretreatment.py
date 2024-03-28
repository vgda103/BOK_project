import os
import json
from konlpy.tag import Mecab
import kss

# 경로의 파일이름을 가저와서 get_str 비교하여 원하는 이름 목록을 얻는다
def get_folder_dir( path, get_str ) -> list:
    """
    경로의 파일들을 가져와 get_str 과 비교하여 get_str 문자가 들어있는 파일이름만 가저옴
    path : 가저올 폴더 경로
    get_str : 파일에서 찾을 문자열 ex : '.txt'
    return : list 형 문자열
    """
    # 폴더의 파일 리스트를 가져온다
    li_file = os.listdir( path )

    # 결과를 저장할 변수
    search = []

    # 피일 리스트 만큼 반복
    for file in li_file:

        # get_str 이 li_file 포함 되어 있으면 True
        if get_str in file:

            # 빈 리스트에 추가
            search.append( file )
            pass # if get_str 끝

    # 저장된 리스트를 반환
    return search
    pass # get_folder_dir 끝


# 읽어온 문장 모음을 JSON 파일로 저장
def save_json( path, data ) -> None:
    """ 
    path : 저장할 경로와 파일 이름
    data : 저장할 데이터. dict 타입

    """
# JSON 파일 저장
    with open( path, 'w', encoding='utf-8' ) as file:
        json.dump( data, file, ensure_ascii=False, indent=4)
    pass # save_json 끝


# json 파일을 읽어온다
def read_json( path ) -> dict:
  """ 
  path : 파일 경로와 이름을 받아서 json 파일을 읽어 딕셔너리 타입으로 반환
  return : 딕셔너리
  """
  # JSON 파일 경로
  file_path = path

  # 파일 열기
  with open(file_path, 'r', encoding='utf-8') as file:
      # data = json.load(file)

      # 파일의 읽고 데이터를 반환
      return json.load(file)

      # 읽어온 데이터를 반환
      # return data
  pass # read_json 끝

# 읽어온 데이터 확인
# print(data)


# 토큰화 
def get_token( text ) -> str:
    """
    문자열을 받으면 그 문자열을 단어로 분리후 태깅을 하여 'NNG', 'NNP', 'VV', 'VA'
    만을 분류하여 문자열로 합처서 반환
    text : 문자열
    """

    # 마캅 생성
    mecab = Mecab( dicpath="C:\mecab" ) # 로컬용
    # mecab = Mecab() # 코랩

    # pos 메소드로 태깅(형태소 분리), 일부 특수문자 등 처리도 시켜줌
    tokens = mecab.pos( text )

    # 형태소 분리된 데이터에 'NNG'(일반명사), 'NNP'(고유명사), 'VV'(동사), 'VA'(형용사) 분류후 저장
    li_token = [ word for word, pos in tokens if pos in [ 'NNG', 'NNP', 'VV', 'VA' ] ]
    filter_str = ' '.join( li_token ) # ' '구분으로 문자열을 합결합

    # 값을 반환
    return li_token
    pass # get_token 끝

# n-gram 
def get_ngram( text, n ) -> list:
    """
    text : 문자열
    n : n 번씩 그룹화
    return : list 
    """
    # 텍스트가 들어올때 토큰화
    tokens = text.split()
    
    # 리스트를 슬라이싱을 사용하여 n-gram을 생성
    ngrams = [ tokens[ i:i+n ] for i in range( len( tokens )-n+1 ) ]
    
    # n-gram을 문자열로 합처서 반환
    return [ ' '.join( ngram ) for ngram in ngrams ]
    pass # ngram


# 의사록의 txt 파일을 읽어와서 토큰화 후 json 파일로 저장한다
# 필요변수 초기화
total_num = 2                       # 분할수
# file_dir = '/content/drive/MyDrive/AI/BOK/Bok_pdf' # 코랩용
file_dir = './Bok_pdf'              # 읽어올 파일 경로
# file_list = os.listdir(file_dir)    # 해당 경로의 폴더의 파일을 리스트로 읽어온다
file_list = get_folder_dir( file_dir, ').txt' ) # 해당 경로의 폴더의 파일중 ').txt'가 포함된 파일을 읽어온다
f_max_num = len(file_list)          # 파일 전체 수? 리스트 길이의 수를 얻는다

document_num = 0                    # 진행 사항 출력에 필요한 변수
document_token = {}                 # 토큰을 저장할 변수
document_sentence = {}              # 문장을 저장할 변수
document= []                        

# total_num 수만큼 반복
for i in range(total_num):

    # j for 문 시작값 얻기
    start_idx = i * ( f_max_num // total_num )
    # 마지막 값을 얻는대 ( i + 1 ) * ( f_max_num // total_num ), f_max_num 중 최소값을 얻는다
    end_idx = min( ( i + 1 ) * ( f_max_num // total_num ), f_max_num )

    # 파일 나누어(start_idx, end_idx) 파일들을 반복한다
    for j in range( start_idx, end_idx ):
        
        # 파일이름 과 경로를 조합
        dir = file_dir + '/' + file_list[ j ]
        # 확장자를 제외한 이름을 얻는다
        name = file_list[ j ][ :-len( '.txt' ) ]
        # print( name )

        # 파일 열기
        f = open( dir, encoding='utf-8' )
        txt_data = f.read()                 # 파일을 일어온다
        f.close()                           # 파일 닫기

        # 문서 초기 단락의 주소를 얻는는다
        if txt_data.find( '( 2 )' ) >= 0:   # '( 2 )' 가 있는 주소를 얻는다
          num = txt_data.find( '( 2 )' )
        elif txt_data.find( '- 2 -' ) >= 0: # '- 2 -' 가 있는 주소를 얻는다
          num = txt_data.find( '- 2 -' )

        # 문서 ( 2 ), '- 2 -'를 기준으로 초기 주소 초기화
        txt_data = txt_data[ num: ]

        # 문장으로 분리
        li_data = kss.split_sentences( txt_data )
        li_data = [ sent.replace('\n','') for sent in li_data ] # \n을 ''로 교체

        # 단어로 분리 한것을 저장할 변수
        filter_str = []

        # 문장(li_data)으로 반복
        for sent in li_data:
            try:
                # 문장을 토큰화 후 변수에 저장
                filter_str.append( get_token( sent ) )
            # 실패시 예외처리
            except Exception as e:
                print(f"An error occurred while processing sentence: { file_list[ j ] } : { sent }")
                print(f"Error message: { e }")
                continue
            pass # for sent 끝
        
        # 읽어온 파일 토큰을 name을 키 값으로 딕셔너리 형으로 저장
        document_token[ name ] = filter_str

        # 진행 사항 출력
        document_num += 1
        print( f'{ document_num } / { f_max_num } 진행중' )

        pass # j for 끝

    # 파일 경로와 파일 명을 조합
    save_dir = '{}/token{:02d}.json'.format( file_dir, i )

    # 파일을 json 형식으로 저장
    save_json( save_dir, document_token )

    pass # i for 끝


# 여러게 json 파일을 읽어서 하나로 데이터를 통합
# 변수 초기화
fiel_data = {}
file_num = 2

# file_num 만큼 반복
for file in range( file_num ):
    file_path = f'./Bok_pdf/token0{ file }.json'
    # print( file_path )

    data_token = read_json( file_path )

    fiel_data.update( data_token )
    # print( data_token.keys() )

    pass # for file


# 딕셔너리에 있는 토큰을 문자열로 합치고 1 ~ 5 까지 n-gram 시켜 파일로 묶는다
# 필요한 변수 초기화
gram_data = {}
str_gram = [ 'uingram', 'bigram', 'trigram', 'fourthgram', 'fifthgram' ]
max_gram = len( str_gram )

# data_token 접근, 파일 > 문서
for key in fiel_data:
    
    # n-gram 결과를 임시로 저장할 변수, 0 ~ 4
    ng_result = [ [], [], [], [], [] ]

    # key값으로 리스트 접근, 문서 > 문장
    for li_data in data_token[ key ]:
        
        # 1 ~ 5 까지 n-gram 반복한다
        for i in range( 0, max_gram ):
            
            # i번 n-gram 시킨 값을 얻는다, i+1 : 1 부터 5 까지
            # 토큰화 된 문장(li_data)을 하나의 문자열로 만든후 n-gram 시킨다
            ngram = get_ngram( ' '.join( li_data ), i+1 )
            
            # i번 시킨 값을 i번 리스트에 추가
            ng_result[i].append( ngram )
            pass # for i 끝

        # 문장을 임시 저장 딕셔너리
        di_temp = {  }

        # 얻은 데이터를 디셔너리에 저장
        for i in range( 0, max_gram ):
            # 데이터를 n-grma 시키면서 같이 처리 하려 했으나 key값이 겹치면 마지막 걸로 최신화됨
            # 또한 같이 리스트에 추가를 시켜 보았을나 하나의 리스트에 추가가 되어
            # 문장 단위로 구분을 할수 없게 됨
            # 따라서 다시 반복문을 돌려 임시 딕셔너리 생성
            # 임시 키 값으로 딕셔너리 생성후 데이터 저장
            di_temp[ str_gram[i] ] = ng_result[i]
            pass # for i 끝

        pass # for li_data 끝

    # 문서 단위로 키값을 주고 임시 딕셔너리에서 값을 저장
    gram_data[ key ] =  di_temp
    
    pass # for key 끝

# 딕셔너리에 있는 토큰을 문자열로 합치고 1 ~ 5 까지 n-gram 시켜 파일로 묶는다
# 필요한 변수 초기화
gram_data = {}
str_gram = [ 'uingram', 'bigram', 'trigram', 'fourthgram', 'fifthgram' ]
max_gram = len( str_gram )

# data_token 접근, 파일 > 문서
for key in fiel_data:
    
    # n-gram 결과를 임시로 저장할 변수, 0 ~ 4
    ng_result = [ [], [], [], [], [] ]

    # key값으로 리스트 접근, 문서 > 문장
    for li_data in data_token[ key ]:
        
        # 1 ~ 5 까지 n-gram 반복한다
        for i in range( 0, max_gram ):
            
            # i번 n-gram 시킨 값을 얻는다, i+1 : 1 부터 5 까지
            # 토큰화 된 문장(li_data)을 하나의 문자열로 만든후 n-gram 시킨다
            ngram = get_ngram( ' '.join( li_data ), i+1 )
            
            # i번 시킨 값을 i번 리스트에 추가
            ng_result[i].append( ngram )
            pass # for i 끝

        # 문장을 임시 저장 딕셔너리
        di_temp = {  }

        # 얻은 데이터를 디셔너리에 저장
        for i in range( 0, max_gram ):
            # 데이터를 n-grma 시키면서 같이 처리 하려 했으나 key값이 겹치면 마지막 걸로 최신화됨
            # 또한 같이 리스트에 추가를 시켜 보았을나 하나의 리스트에 추가가 되어
            # 문장 단위로 구분을 할수 없게 됨
            # 따라서 다시 반복문을 돌려 임시 딕셔너리 생성
            # 임시 키 값으로 딕셔너리 생성후 데이터 저장
            di_temp[ str_gram[i] ] = ng_result[i]
            pass # for i 끝

        pass # for li_data 끝

    # 문서 단위로 키값을 주고 임시 딕셔너리에서 값을 저장
    gram_data[ key ] =  di_temp
    
    pass # for key 끝

# 결과물 저장
file_path = f'./Bok_pdf/ngram.json'

save_json( file_path, gram_data )