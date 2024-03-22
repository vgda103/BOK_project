from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

OldDate = '20210101'
today = datetime.now()
NowDate = today.strftime('%Y%m%d')
datas = []
page_num = 1
while True:
    url = f'https://www.korcham.net/nCham/Service/EconBrief/appl/ProspectBoardList.asp?board_type=1&pageno={page_num}&daybt=OldNow&m_OldDate={OldDate}&m_NowDate={NowDate}'
    res = requests.get(url)  
    soup = BeautifulSoup(res.content.decode('euc-kr','replace'), 'html.parser')
    if soup.select_one('table tr').text == ' * 등록된 데이터가 없습니다. ':
        break
    else:
        table = soup.select('table tr')
        headers = [th.text.strip() for th in soup.select('table tr th')]
        page_datas = []
        for row in table[1:]:
            daily_data = []
            daily_data.extend(td.text.strip() for td in row)
            page_datas.append(daily_data)
        datas.extend(page_datas)
        page_num += 1

daily_call_rate = pd.DataFrame(datas, columns=headers)
daily_call_rate.to_csv('daily_call_rate.csv', index=False)