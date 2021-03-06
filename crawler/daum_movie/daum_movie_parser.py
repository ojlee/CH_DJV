from bs4 import BeautifulSoup
import os
from datetime import datetime
from selenium import webdriver
import csv
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daum_movie_db.settings")

import django
django.setup()

from parsed_data.models import Movie


#파일 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#크롬 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")

# driver = webdriver.Chrome(str(BASE_DIR) +'\chromedriver', chrome_options=options)
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(2)

#다음영화 접근
driver.get('http://movie.daum.net/main/new#slide-1-0')


def crawl(movie):
    if movie == 'title':
        print('return')
        return
    
    #찾으려는 영화
    target_movie = " "
    target_movie = movie

    #다음영화 검색
    serch_word = ""
    serch_word = target_movie
    serch_box = driver.find_element_by_id('tfSearch')
    serch_box.send_keys(serch_word)
    serch_box.submit()

    #검색 결과에서 첫번째 글에 접근
    page_list = ""
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "movie_result")))
    sr_num = driver.find_element_by_xpath('//*[@id="movie_result"]/strong/span')

    if sr_num.text == '1':
        page_list = driver.find_element_by_xpath('//*[@id="contents_result"]/li/a[1]')
    else:
        page_list = driver.find_element_by_xpath('//*[@id="contents_result"]/li[1]/a[1]')
    page_list.click()

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

    # #제목
    # for movie_title in mv_title:
    #     target_title = movie_title.get_text()
    #     target_title = target_title.replace(" ", "")  ##공백제거
    #     target_title = re.sub("[(].*[)]", "", target_title)  ## (연도)포함 괄호 내부 내용 제거
    #     target_title = re.sub("[-:]", " ", target_title)  ## "-" 과 ":"은 공백으로
    #     target_title = re.sub("[.]", "", target_title)  ## "."은 제거
        
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
            target_nation = target_nation.replace(" ", "")
            target_nation = target_nation.replace("\t", "")
            print(target_nation)

        #개봉일
        elif info_code == 2 :
            if categorize.text.strip()[7:8] == "." :
                target_premiere = datetime.strptime(categorize.text.strip()[:10],'%Y.%m.%d')
            elif categorize.text.strip()[4:5] == "." :
                target_premiere = datetime.strptime(categorize.text.strip()[:7],'%Y.%m') #개봉일자가 월까지만 나와있는 경우 = 1일자로 개봉한 것으로 출력 됨
            else :
                target_premiere = None #개봉일자 없는 경우

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
    if len(people) != 1:
        target_actor = people[1]
    else:
        target_actor = None
    if len(people) > 2:
        for prt in range(2, len(people)):
            if prt != 0:
                target_actor = target_actor + ',' + people[prt]

    #DB에 저장
    Movie(title=target_movie,grade=target_grade, genre=target_genre, nation=target_nation, premiere=target_premiere, director=target_director, actor=target_actor).save()



#db 초기화
queryset = Movie.objects.all()
queryset.delete()

#편성표 상의 영화 정보 수집(합쳐지고 중복은 제거된 리스트)
uni = open('union_sche4.csv', 'r', encoding='utf-8')
rdr_uni = csv.reader(uni, delimiter=',', quotechar='"')
index = 1
for movie_list in rdr_uni:
    print(str(index) + " // " + str(movie_list))
    crawl(movie_list[1])
    index += 1
uni.close()

print("done!") #작업이 완료 되면 done 출력

#드라이버 종료
driver.quit()
