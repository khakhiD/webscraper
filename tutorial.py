import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# request를 이용하여 "https://library.gabia.com/" 주소로 GET 요청을 보내고 응답을 받는다.
# 상대 코드와 HTML 내용을 응답(REQUEST)받을 수 있다.
page = requests.get("https://library.gabia.com/")

# 응답받은 HTML 내용을 BeautifulSoup 클래스의 객체 형태로 생성/반환한다.
# bs 객체를 통해 html 코드를 파싱하기 위한 여러 가지 기능을 사용할 수 있다.
# (request.text는 응답받은 내용(html)을 Unicode 형태로 반환한다.)
soup = bs(page.text, "html.parser")

# bs가 제공하는 기능 중 CSS 셀렉터를 이용하여 원하는 정보를 찾는 기능이다.
# div.esg-entry-content a > span은 esg-entry-content 클래스로 설정된 div 태그들의
# 하위에 존재하는 a 태그, 그 하위에 존재하는 span 태그를 의미하고, 이 셀렉터를 이용하여
# 가비아 라이브러리 홈페이지에 존재하는 포스터들의 제목을 추출할 수 있다.

elements = soup.select('div.esg-entry-content a.eg-grant-element-0')

# 제목(titles)과 링크(links) 배열에 요소를 추가한다.
titles = []
links = []

for index, element in enumerate(elements, 1):
    titles.append(element.text)
    links.append(element.attrs['href'])

# titles와 links 배열 값으로 Pandas의 DataFrame을 생성한다.
df = pd.DataFrame()
df['게시글 제목'] = titles
df['링크'] = links

# to_excel() 함수를 이용하여 엑셀 파일을 작성한다.
df.to_excel('xlsx/library_gabia.xlsx',
            sheet_name='Sheet1',
            encoding='utf-8',
            na_rep = '',
            inf_rep = '',
            index = False
)