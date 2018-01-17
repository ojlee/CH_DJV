from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
driver = webdriver.Chrome(str(BASE_DIR) +'\chromedriver')
driver.implicitly_wait(3)

#구글에 접근
driver.get('https://www.google.co.kr')

#찾으려는 영화
target_movie = '신과함께(2017)' #나중에는 DB에서 가져올 예정

#구글 검색
serch_word = 'Daum 영화 ' + target_movie
serch_box = driver.find_element_by_id('lst-ib')
serch_box.send_keys(serch_word)
serch_box.submit()

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

data = {}

for movie_title in mv_title:
    title = movie_title.get_text()

for movie_grade in mv_grade:
    grade = movie_grade.get_text()

for info in mv_info:
    person = info.find_all("a", class_ = "link_person #info #name")
    sundry_info = info.find_all("dd")

info_code = 0
for categorize in sundry_info:
    if info_code == 0 :
        genre = categorize.text.strip()
    elif info_code == 1 :
        nation = categorize.text.strip()
    elif info_code == 2 :
        premiere = categorize.text.strip()[:10]
    else :
        break
    info_code = info_code + 1

#제목
data["제목"] = title

#평점
data["평점"] = grade

#장르
data["장르"] = genre

#국가
data["국가"] = nation

#개봉일
data["개봉일"] = premiere

#인물정보
people = {}
a = 0
for name in person:
    people[a] = name.get_text()
    a = a + 1
    
#감독
data["감독"] = people[0]

#주연
actor = people[1]
for prt in range(2, len(people)):
    if prt != 0:
        actor = actor + ',' + people[prt]
        data["주연"] = actor

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file, ensure_ascii=False)
