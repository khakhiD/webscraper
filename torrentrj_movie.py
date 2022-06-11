from matplotlib import dates
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

titles = []
size = []
date = []
links = []
download = []

for page_num in range(10):
    url = f'https://torrentrj39.com/v-1?page={page_num+1}'
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    elements = soup.select('div.topic-item')
    
    for i, e in enumerate(elements, 1):
        t = e.select_one('div.ti2 > a.tit').attrs['title']
        s = e.select_one('div.ti3').text
        d = e.select_one('div.ti4').text
        l = 'https://torrentrj39.com'+e.select_one('a.tit').attrs['href']

        titles.append(t)
        size.append(s)
        date.append(d)
        links.append(l)
        
        l_soup = bs(requests.get(l).text,'html.parser')
        
        if (l_soup.select_one('a[class="btn main_bg btn-sm"]')) is None:
            print("***************해당 게시글은 다운로드가 없음**************\n")
            download.append('-')
            continue
        else:
            dl = 'https://torrentrj39.com'+l_soup.select_one('a[class="btn main_bg btn-sm"]').attrs['href']
            download.append(dl)
            
        print("\n페이지:"+str(page_num+1)+"번호:"+str(i))
        print(str(t)+" ")
        print(str(s)+" ")
        print(str(d)+" ")
        print(str(l)+" ")
        print(str(dl)+" ")


df = pd.DataFrame()
df['제목'] = titles
df['용량'] = size
df['날짜'] = date
df['링크'] = links
df['다운'] = download

df.to_excel('xlsx/torrentrj_movie.xlsx',
            sheet_name='Sheet1',
            encoding='utf-8',
            na_rep = '',
            inf_rep = '',
            index = False
)