from datetime import datetime
from matplotlib import dates
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

TIME = datetime.now()
URL = 'https://torrentrj39.com/v-1?page='
PATH = 'webscraper/xlsx/'
FNAME = 'TorrentRJ_drama_' + TIME.strftime('%y-%m-%d_%H-%M') + '.xlsx'
titles = []
size = []
date = []
links = []
download = []

def save_xsxl():
    df = pd.DataFrame()
    df['제목'] = titles
    df['용량'] = size
    df['날짜'] = date
    df['링크'] = links
    df['다운'] = download
    
    df.to_excel(PATH + FNAME, sheet_name = 'new_movie', encoding = 'utf-8', index = False)

def array_append(a,b,c,d):
    titles.append(a)
    size.append(b)
    date.append(c)
    links.append(d)
    dl_soup = bs(requests.get(d).text,'html.parser')
    if (dl_soup.select_one('a[class="btn main_bg btn-sm"]')) is None:
        e = 'none'
        download.append('-')
        return
    else:
        e = 'https://torrentrj39.com' + dl_soup.select_one('a[class="btn main_bg btn-sm"]').attrs['href']
        download.append(e)

    print(str(a)+'\n'+str(b)+'\n'+str(c)+'\n'+str(d)+'\n'+str(e)+'\n')

def page_scraping(num):
    for page_num in range(num):
        url = URL + str(page_num+1)
        req = requests.get(url)
        soup = bs(req.text, 'html.parser')
        elements = soup.select('div.topic-item')
        
        for i, e in enumerate(elements, 1):
            t = e.select_one('div.ti2 > a.tit').attrs['title']
            s = e.select_one('div.ti3').text
            d = e.select_one('div.ti4').text
            l = 'https://torrentrj39.com'+e.select_one('a.tit').attrs['href']
            print("페이지: "+ str(page_num+1)+"\t번호: "+str(i))
            array_append(t,s,d,l)
    save_xsxl()

if __name__ == "__main__":
    page_scraping(5)


