from bs4 import BeautifulSoup
import os
from datetime import datetime
from selenium import webdriver

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daum_movie_db.settings")

import django
django.setup()

from parsed_data.models import Movie

#찾으려는 영화
target_movie = '뷰티인사이드' #나중에는 DB에서 가져올 예정

#파일 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#크롬 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(str(BASE_DIR) +'\chromedriver', chrome_options=options)
driver.implicitly_wait(3)

#구글에 접근
driver.get('http://www.google.co.kr')

#구글 검색
serch_word = 'Daum 영화 ' + target_movie
serch_box = driver.find_element_by_id('lst-ib')
serch_box.send_keys(serch_word)
serch_box.submit()

#검색 결과에서 첫번째 글에 접근
page_list = driver.find_element_by_xpath("//div[@id='rso']/div/div")
target_page = page_list.find_element_by_tag_name('a')
target_page.click()

#html 얻기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
mv_info = soup.select(
    '#mArticle > div.detail_movie.detail_main > div.movie_detail > div.movie_basic > div.main_detail > div.detail_summarize > div > dl.list_movie.list_main'
    )
mv_title = soup.select(
    '#mArticle > div.detail_movie.detail_main > div.movie_detail > div.movie_basic > div.main_detail > div.detail_summarize > div > div.subject_movie > strong'
    )
mv_grade = soup.select(
    '#mArticle > div.detail_movie.detail_main > div.movie_detail > div.movie_basic > div.main_detail > div.detail_summarize > div > div.subject_movie > a > em'
    )

#제목
for movie_title in mv_title:
    target_title = movie_title.get_text()
    
#평점
for movie_grade in mv_grade:
    target_grade = float(movie_grade.get_text())

for info in mv_info:
    person = info.find_all("a", class_ = "link_person #info #name")
    sundry_info = info.find_all("dd")

info_code = 0
for categorize in sundry_info:
    #장르
    if info_code == 0 :
        target_genre = categorize.text.strip()

    #국가
    elif info_code == 1 :
        target_nation = categorize.text.strip()

    #개봉일
    elif info_code == 2 :
        target_premiere = datetime.strptime(categorize.text.strip()[:10],'%Y.%m.%d')

    else :
        break
    info_code = info_code + 1


#인물정보
people = {}
a = 0
for name in person:
    people[a] = name.get_text()
    a = a + 1

#감독
target_director = people[0]

#주연
target_actor = people[1]
for prt in range(2, len(people)):
    if prt != 0:
        target_actor = target_actor + ',' + people[prt]

#DB에 저장
Movie(title=target_title,grade=target_grade, genre=target_genre, nation=target_nation, premiere=target_premiere, director=target_director, actor=target_actor).save()
