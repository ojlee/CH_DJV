
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from datetime import datetime
import re
import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "m_schedule.settings")
import django
django.setup()

from crawl_sche.models import OcnSchedule
from crawl_sche.models import CgvSchedule
from crawl_sche.models import SActionSchedule

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

##윈도우용
# cDriverpath = chrome_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver_win32/chromedriver')
# driver = webdriver.Chrome(chrome_options=options)

##리눅스용
driver = webdriver.Chrome(chrome_options=options)

year = 0

##db 초기화 함수
def dbinit():
    print('이전 데이터 삭제중')
    queryset = OcnSchedule.objects.all()
    queryset.delete()
    queryset = CgvSchedule.objects.all()
    queryset.delete()
    queryset = SActionSchedule.objects.all()
    queryset.delete()

##페이지 접속 함수
def connect():
    driver.implicitly_wait(2)
    driver.get('https://www.hcn.co.kr/ur/bs/ch/channelInfo.hcn?method=man_00&p_menu_id=1903')  # 페이지 접속
    driver.find_element_by_xpath('//*[@id="genreList"]/li[3]/a').click()  # 영화탭

##채널목록
def list_ch():
    return [
        ['OCN','//*[@id="chList"]/li[4]/a'],
        ['CGV','//*[@id="chList"]/li[2]/a'],
        ['SUPER ACTION','//*[@id="chList"]/li[6]/a']
    ]


##연도체크 함수
def check_year(date,year):
    if re.compile('12월31일').match(date[0].text.strip()) != None:
        year -= 1
    return year

##제목가공 함수 - 공백, 부 제거
def title_cutting(title):
    title = title.replace(" ", "") ##공백제거
    title = re.sub("\d부$", "", title) ##부 제거
    title = re.sub("[(].*[)]", "", title) ## (연도)포함 괄호 내부 내용 제거
    title = re.sub("[-:]", " ", title) ## "-" 과 ":"은 공백으로
    title = re.sub("[.]", "", title) ## "."은 제거
    return title

##제목 필터링 조건 함수
def title_filtering(ctitle, ptitle):
    #필터
    term = ['크리미널마인드', '코미디빅리그' ,'38사기', '나인뮤지스', '청춘무비', '악의도시' ,'FC', 'CSI', 'NCIS', '멘탈리스트', 'SVU', '시즌', '비하인드', '시상식', '주말N', '무비버스터즈', '무비멘터리', '액션매니악']

    #필터링
    for i in range(0, len(term)):
        p = re.compile('^.*'+term[i]+'.*$')
        if p.search(ctitle) != None:
            return False

    #바로 직전과 달라도 탈락
    if ctitle != ptitle:
        return True

    return False


## 긁기함수 딕션{채널 제목 상영시간 날짜} 반환
def scrap(cur_ch):
    html = driver.page_source
    soup = bs(html, 'html.parser')
    title = soup.select('td.left > span > a') ##프로그램 제목
    time = soup.select('td.f > strong') ##방영시간
    date = soup.select('div.dateSelector > ul > li:nth-of-type(2) > a') ##월일

    ## 자료형 맞춰주기
    global year
    year = check_year(date, year)
    infopac = []
    for i in range(0, len(title)):
        title[i] = title_cutting(title[i].text)##제목가공(str)

        if title_filtering(title[i], title[i-1]): ##중복 영화막기
            info = []
            info.append(cur_ch[0])
            info.append(title[i])
            info.append(datetime.strptime(time[i].text, '%H:%M'))
            datenum = re.findall('\d+', date[0].text.strip())
            yeardate = str(year) + '-' + datenum[0] + '-' + datenum[1]  ##날짜를 출력
            info.append(datetime.strptime(yeardate, '%Y-%m-%d'))
            infopac.append(info)
    return infopac


##db에 담는함수(infopac받아서)
def save_db(infopac):
    for info in infopac:
        if info[0] =='OCN':
            OcnSchedule(ch=info[0], title=info[1], time=info[2], date=info[3]).save()
        elif info[0] =='CGV':
            CgvSchedule(ch=info[0], title=info[1], time=info[2], date=info[3]).save()
        elif info[0] == 'SUPER ACTION':
            SActionSchedule(ch=info[0], title=info[1], time=info[2], date=info[3]).save()
        else:
            print('잘못된 채널, table 없음')

## 채널변경 함수/ loop모드일때 마지막 채널이면 프로그램 종료
def move_ch(cur_ch, mod):
    if mod == 'init':
        cur_ch = list_ch()[0]
        driver.find_element_by_xpath(cur_ch[1]).click()
        print('현재채널 :  ' + cur_ch[0])
        return  cur_ch
    elif mod == 'loop':
        if cur_ch != list_ch()[-1]:
            cur_ch = list_ch()[list_ch().index(cur_ch)+1]
            driver.find_element_by_xpath(cur_ch[1]).click()
            print('현재채널 :  ' + cur_ch[0])
            return cur_ch
        else:
            print('더이상 채널목록이 없습니다')
            print('수집이 종료되었습니다')
            sys.exit()

def progressBar(value, endvalue, bar_length):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


if __name__=='__main__':
    dbinit()
    connect()
    global year
    year = int(time.ctime().split(' ')[-1])  ##올 해 설정
    cur_ch = ''
    cur_ch = move_ch(cur_ch, 'init')
    save_db(scrap(cur_ch)) ##db에 담기(긁어오기)

    ## 반복 더이상 긁어올게 없을때까지
    while True:
        value = 0
        while True:
            progressBar(value, 730, 20)
            # driver.implicitly_wait(1)
            # explicitly wait 최대 10초까지 기다려줌
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Content"]/form/div[7]/a[1]/img')))

            driver.find_element_by_xpath('//*[@id="Content"]/form/div[7]/ul/li[1]/a').click()  ##전날짜
            driver.find_element_by_xpath('//*[@id="Content"]/form/div[7]/a[1]/img').click()    ##이전날짜 더보기
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sheetTable')))
            infoset = scrap(cur_ch) #긁어오기
            value += 1
            if infoset != []:    #긁을것이 있는지 검사 없으면 채널변경
                save_db(infoset)  ##db에 담기
            else:
                break
        connect()
        cur_ch = move_ch(cur_ch, 'loop')    ##채널변경
        year = int(time.ctime().split(' ')[-1])