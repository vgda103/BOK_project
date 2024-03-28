from Crawling.Crawling import Crawling
from pdf_red.Red_pdf import Red_pdf
import os

class BOK_pdf( Crawling, Red_pdf ):

    def __init__(self) -> None:
        """
        생성자
        import : Crawling, Red_pdf
        부모 import
        requests, json, bs4, BeautifulSoup, fitz
        """
        super().__init__()
    pass

    def Get_pdf( self, path, star, end ) -> None:
        """
        star 시작 페이지 부터 end 페이지 까ㅣ지 해당 사이트의 pdf 파일을 다운 받는다
        path : 파일 경로
        star : 시작 페이지 1부터 시작
        end : 끝 페이지
        """

        # star 가 0보다 작거나 같음 리턴
        if star <= 0:
            return None
        
        # 기본 접속 주소
        Source_URL = 'https://www.bok.or.kr'

        # 페이지 반복문
        for i in range( star, end + 1 ):

            # 접속 주소 가져온다
            page_URL = Source_URL + f"/portal/bbs/B0000245/list.do?menuNo=200761&pageIndex={i}"

            # 접속 주소 출력
            print( page_URL )

            # 페이지 접속
            self.url_get( page_URL )
            
            # 가져온 데이터를 파싱
            get_html = self.get_parser()
            # a 태그의 데이터를 가져온다
            get_a = get_html.find_all( 'a' )
            
            # 필요 변수 선언
            adres = None    # 주소
            num = 0         # 몇번째 진행인지 알려주는 변수
            file_name = ''  # 파일 이름

            # a 데이터중 필요 데이터 추출 반복문
            for tag in get_a:

                # 좀더 다루기 쉬운 문자열로 변환
                temp = str( tag )
                
                # 문자열 중 titlesub가 있는지 찾는다. 이름을 얻는 곳
                if temp.find( 'titlesub' ) >= 0:
                    # titlesub가 있으면 해당 테그를 저장
                    adres = str( tag )
                    # 테그의 시작 주소와 끝 주소를 찾는다
                    num_star = temp.find( 'titlesub' ) + len('titlesub">')
                    num_end = temp.find('</span>')# - len( '(2024.2.22)' )

                # 테그중 필요한 것이 아니면 넘긴다
                # if not( temp.find( 'hwp' ) >= 0 or temp.find( 'pdf' ) >= 0 ): # 나중에 hwp 도 필요하면 주석해제
                if not( temp.find( 'pdf' ) >= 0 ):  # pdf 파일이 아니면 넘긴다
                    continue

                # 접속 리퀘스트 얻는다
                URL = Source_URL + tag[ 'href' ]    # 받을 파일의 링크를 조합
                
                # 링크 접속
                self.url_get( URL )
                
                # 파일 이름 조립
                file_path01 = path + adres[ num_star:num_end ] + '.pdf'
                # 이름만 따로 관리하는 변수
                file_name += adres[ num_star:num_end ] + '\n'
                
                # 지정된 경로에 디렉토리 생성
                os.makedirs( path, exist_ok=True )

                # pdf 파일 저장
                f = open( file_path01, 'wb')
                f.write( self.respoonse.content )
                f.close()
                
                # 몇번째 출력인지 알려주는 변수
                num += 1

                # 진행 출력
                print( f'{num}번 실행중' )                
            # break
            pass # for i 끝

            # 이름만 따로 관리할 파일에 저장
            # 파일 경로 조합
            file_path02 = path + 'name.txt'
            # 파일 저장
            f = open( file_path02, 'a' )
            # print( type( file_name ) )
            f.write( file_name )
            f.close()
            
            # 총진행 상황, 페이지 진행 출력
            print( f'{i}페이지 끝 : {i} / {end}' )       
        pass # BOK_connect 끝

    def get_str( self, path ) -> str:
        """
        지정된 경로의 pdf 파일들으 읽어와 리스트 없이 한문자열로 반환해준다.
        path : 파일 경로
        return : str
        """

        file_str = ''   # 모든 파일들의 내용을 받을 변수
        num = 0         # 진행상황을 알려주는 변수

        # 지정된 경로의 파일들 리스트를 가져오는 변수
        file_list = os.listdir( path )

        # 가저온 파일 목록 만큼 반복
        for file in file_list:
            # 파일 경로 조합
            file_path = f'{path}{file}'

            # 예외 처리문 
            try:
                # 파일을 연다
                with open(file_path, 'rb') as f:
                    # pdf 파일을 열어서 \n을 \t 으로 교체후 끝에 \n을 추가 후 파일을 문자열에 추가
                    file_str += self.opne_pdf(file_path).replace('\n', '\t') + '\n'

            # 파일을 못찾았을 경우 에러 처리
            except FileNotFoundError:
                print(f"File {file_path} not found.")
            
            # 예상치 못한 에러를 처리 하는 곳
            except Exception as e:
                print(f"An error occurred while processing {file_path}: {e}")
            
            # 정상 작동시 처리되는 곳
            else:
                # 진행 사항을 업데이트
                num += 1
                print( f'{ num } / { len( file_list ) } 진행중' )
        # 문자열을 반환 하고 끝
        return  file_str
        pass # get_str 

    def to_txtfile( self, path ) -> None:
        """
        지정된 경로의 pdf 파일들으 읽어와 pdf를 txt파일로 저장하고 작성일, pdf이름, txt이름의 index.txt 파일 생성
        path : 파일 경로
        """

        # file_str = ''   # 모든 파일들의 내용을 받을 변수
        num = 0         # 진행상황을 알려주는 변수

        # 지정된 경로의 파일들 리스트를 가져오는 변수
        file_list = os.listdir( path )

        # 가저온 파일 목록 만큼 반복
        for file in file_list:
            # print( type(file) )

            # pdf 파일이 아니면 
            if not ( file.find( '.pdf' ) >= 0 ):
                print( "건너뜀" )
                continue

            # # 파일 경로 조합
            # file_path = f'{path}{file}'
                    
            txt_name = file[ :-len( '.pdf' ) ]  # 확장자를 제외한 파일이름을 얻는다
            num = file.rfind( '(' )             # 뒤에서부터 ( 찾는다
            date = txt_name[ num: ]             # 날짜를 얻는다, 괄호부터 끝까지 내용을 얻는다
            txt_name += '.txt'                  # 텍스트파일저장 이름과 확장자 추가
            # 인덱스에 저장할 내용 조합
            index_str = date + '\t' + file + '\t' + txt_name + '\n'

            # 예외 처리문 
            try:
                # 파일을 연다
                with open( path + file , 'rb') as f:
                    # pdf 파일을 열어서 \n을 \t 으로 교체후 끝에 \n을 추가 후 파일을 문자열에 추가
                    file_str = self.opne_pdf( path + file )
            # 파일을 못찾았을 경우 에러 처리
            except FileNotFoundError:
                print(f"File { path + file } not found.")
            # 예상치 못한 에러를 처리 하는 곳
            except Exception as e:
                print(f"An error occurred while processing { path + file }: {e}")
            # 정상 작동시 처리되는 곳
            else:
                print( 'pdf 읽어옴' )
                pass

            # 예외 처리문
            try:
                # 파일 열기 
                with open( path + txt_name, 'w' ) as txt_f:
                    txt_f.write( file_str ) # txt 파일 저장
            # 파일을 못찾았을 경우 에러 처리
            except FileNotFoundError:
                print(f"File { path + txt_name } not found.")
            # 예상치 못한 에러를 처리 하는 곳
            except Exception as e:
                print(f"An error occurred while processing { path + txt_name }: {e}")
            # 정상 작동시 처리되는 곳
            else:
                print( 'txt 변환' )
                pass
            
            # 예외 처리문
            try:
                # 파일 열기 
                with open( path + 'index.txt', 'a' ) as idx_F:
                    idx_F.write( index_str ) # index txt 파일 저장
            # 파일을 못찾았을 경우 에러 처리
            except FileNotFoundError:
                print(f"File {  path + 'idex.txt' } not found.")
            # 예상치 못한 에러를 처리 하는 곳
            except Exception as e:
                print(f"An error occurred while processing {  path + 'idex.txt' }: {e}")
            # 정상 작동시 처리되는 곳
            else:
                print( '목록 추가' )
                pass
        
            # 진행 사항을 업데이트
            num += 1
            print( f'{ num } / { len( file_list ) } 진행중' )
        pass # to_txtfile 끝

Bok = BOK_pdf()
Bok.Get_pdf( './Bok_pdf/', 1, 20 ) # 경로, 시작페이지, 마지마막페이지
Bok.to_txtfile( './Bok_pdf/' )
