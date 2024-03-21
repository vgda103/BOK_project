# 만들었던 크롤링 부분을 클레스화?
# 정의
import requests
import json
from bs4 import BeautifulSoup

# Crawling
class Crawling:

    respoonse = None

    def __init__(self) -> None:
        """
        생성자
        """
        self.respoonse = requests
        
        # return self
        pass # 생성자 끝

    def get_requests( self ):
        return self.respoonse


    def url_get( self, URL, headers = {}, data = {}, verify=True ) -> int:
        """
        URL : str, 접속할 사이트주소
        headers : 사이트에서 원하는 해더 타입 입력 기본값은 빈 딕셔너리
        data : 사이트에서 원하는 데이터 타입 기본값은 빈 리스트
        reutnr : int, respoonse 상태를 알려준다.
        """

        # 사이트에 요청
        self.respoonse = requests.get( URL, headers = headers, params = data, verify = verify )
        return self.get_states()        
        pass # 메소드 get_connect
    
    def url_post( self, URL, headers = {}, data = {} ) -> int:
        """
        URL : str, 접속할 사이트주소
        headers : 사이트에서 원하는 해더 타입 입력 기본값은 빈 딕셔너리
        data : 사이트에서 원하는 데이터 타입 기본값은 빈 리스트
        reutnr : int, respoonse 상태를 알려준다.
        """

        # 사이트에 요청
        self.respoonse = requests.post( URL, headers = headers, params = data )
        return self.get_states()        
        pass # 메소드 get_connect

    def get_states( self ) -> int:
        """
        respoonse 상태를 알려준다.
        """
        return self.respoonse.status_code
        pass # get_res_states 

    def get_text( self ) -> str:
        """
        respoonse의 속성의 텍스트를 넘겨준다
        """
        return self.respoonse.text
        pass # get_text 끝

    def get_to_json( self ):
        """
        load를 사용하니 사용하지 말것
        load는 파일에서 읽어올때 사용함
        loads는 문자열을 읽을때 사용함
        respoonse를 json 형태로 파싱한 데이터를 넘겨준다
        """
        # j_data = json.loads( self.respoonse.text )
        return json.load( self.respoonse.text )
        pass # get_to_json 끝
    
    def get_to_jsons( self ):
        """
        loads를 사용함
        load는 파일에서 읽어올때 사용함
        loads는 문자열을 읽을때 사용함
        respoonse를 json 형태로 파싱한 데이터를 넘겨준다
        """
        # j_data = json.loads( self.respoonse.text )
        return json.loads( self.respoonse.text )
        pass # get_to_json 끝
    
    def get_to_soup( self ):
        """
        respoonse를 BeautifulSoup 형태로 파싱한 데이터를 넘겨준다
        """
        return BeautifulSoup( self.respoonse.text, 'html.parser' )
        pass # get_to_soup 끝

    def get_parser( self ):

        get_str = self.respoonse.text[ :100 ]

        if get_str.find( '<!DOCTYPE HTML>' ):
            return self.get_to_soup()
            pass

        elif get_str.find( '{' ):
            return self.get_to_jsons()
        
        else:
            return self.get_text()
            pass
        pass # get_parser 끝

    pass # class Crawling 끝