import fitz

class Red_pdf:

    def __init__(self) -> None:
        """
        생성자
        import : fitz
        """
        pass # __init__ 끝

    def opne_pdf( self, path ) -> str:
        """
        path : pdf 파일 경로
        return : str(문자열)
        """

        doc = fitz.open( path )

        # pdf 파일을 저장할 문자타입
        text = ''

        # 1패이지씩 읽어올 반복문
        for page in doc:
            # 1패이지씩 읽어서 text 저장
            text += page.get_text()
            pass # for page 끝

        return text
        pass # opne_pdf 끝

    pass