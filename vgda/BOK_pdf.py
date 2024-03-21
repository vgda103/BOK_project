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

    def Get_pdf( self, path, star, end ):
        """
        star : 시작 페이지 1부터 시작
        end : 끝 페이지
        """
        if star <= 0:
            return None
        
        Source_URL = 'https://www.bok.or.kr'

        for i in range( star, end + 1 ):
            # 접속 주소
            page_URL = Source_URL + f"/portal/bbs/B0000245/list.do?menuNo=200761&pageIndex={i}"

            print( page_URL )

            self.url_get( page_URL )

            # print( self.get_text() )
            
            get_html = self.get_parser()
            get_a = get_html.find_all( 'a' )
            
            adres = None

            num = 0
            file_name = ''

            for tag in get_a:

                temp = str( tag )
                
                if temp.find( 'titlesub' ) >= 0:
                    adres = str( tag )
                    num_star = temp.find( 'titlesub' ) + len('titlesub">')
                    num_end = temp.find('</span>')# - len( '(2024.2.22)' )

                # if not( temp.find( 'hwp' ) >= 0 or temp.find( 'pdf' ) >= 0 ):
                if not( temp.find( 'pdf' ) >= 0 ):
                    continue
                
                # print( type( tag.text ) )
                # print( tag.text )
                temp = tag.text

                temp = temp.replace('\t', "")
                temp = temp.replace('\n', "")
                temp = temp.replace('\n ', "")[1:]
                # break

                file_get = Crawling()
                URL = Source_URL + tag[ 'href' ]
                
                file_get.url_get( URL )

                file_path01 = path + adres[ num_star:num_end ] + '.pdf'
                file_name += adres[ num_star:num_end ] + '\n'
                
                # 지정된 경로에 디렉토리 생성
                os.makedirs( path, exist_ok=True )
                f = open( file_path01, 'wb')
                f.write( file_get.respoonse.content )
                f.close()

                num += 1

                print( f'{num}번 실행중' )                
            # break
            pass # for i

            file_path02 = path + 'name.txt'
            f = open( file_path02, 'w' )
            # print( type( file_name ) )
            f.write( file_name )
            f.close()
            
            print( f'{i}페이지 끝 : {i} / {end}' )
        
        pass # BOK_connect 끝