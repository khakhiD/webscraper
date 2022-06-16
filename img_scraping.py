# 네이버 이미지 검색 스크래핑
from click import option
import os, re, time, dload
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sqlalchemy import null
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

def create_dir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else: return
    except OSError:
        print("Error: Failed to create the directory.")

def index_ext(path):
    file_list = os.listdir(path)
    if len(file_list) != 0:
        for i in range(len(file_list)):
            file_list[i] = re.sub(r'[^\d]', '', file_list[i])
        return int(max(file_list))+1
    else:
        return 1
        
def img_scraping(keyword, dir_path, name):
    create_dir(dir_path + name)
    url = f'https://search.naver.com/search.naver?where=image&sm=tab_jum&query={keyword}'
    
    # Selenium driver set-up
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # url get
    browser.get(url)
    time.sleep(3)

    # html parsing
    req = browser.page_source
    soup = bs(req, 'html.parser')
    images = soup.select('.sp_nimage .photo_tile .photo_bx .link_thumb>img')
        
    index = index_ext(dir_path + name)
    
    # image saving
    for image in images:
        img = image['src']
        if dload.save(img, f'{dir_path}/{name}/{name}{index}.jpg'):
            print(f'{name}{index}.jpg has been saved successfully.')
            index += 1
    browser.quit()


# path set-up
dir_path = 'N:/. Personal_folder/2022-1__컴공_관련/머신러닝프로그래밍/기말과제_CNN_이미지분류/custom_datasets/'
img_scraping("고양이", dir_path, "cat")


# https://velog.io/@sangyeon217/deprecation-warning-executablepath-has-been-deprecated
# https://velog.io/@chacha/%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%9E%90%EB%8F%99%ED%99%94-tool-%EC%A0%95%EB%A6%AC-2%ED%83%84-Selenium-jkk58zqj1c
# https://pypi.org/project/dload/
# https://hyunjungchoi.tistory.com/47
# https://velog.io/@choi46910/%EC%86%A1%EA%B0%95-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%9B%B9%EC%8A%A4%ED%81%AC%EB%9E%98%ED%95%91%ED%81%AC%EB%A1%A4%EB%A7%81
# re 모듈 https://yunwoong.tistory.com/140
# 정규표현식 https://wikidocs.net/4308
# 디렉토리 생성 https://gentlesark.tistory.com/90



'''
추가해야할 것?
 - 깃허브 자동 커밋..?
 - 입력 변수로 키워드 주고 url 알아서 따오기
'''