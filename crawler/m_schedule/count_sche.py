import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "m_schedule.settings")
import django
django.setup()

from crawl_sche.models import OcnSchedule
from crawl_sche.models import SActionSchedule
from crawl_sche.models import CgvSchedule

from crawl_sche.models import resultOcn
from crawl_sche.models import resultCgv
from crawl_sche.models import resultSAction



Ocnmovies = OcnSchedule.objects.all()
Cgvmovies = CgvSchedule.objects.all()
SActionSchedule = SActionSchedule.objects.all()

def dbinit():
    print('이전 데이터 삭제중')
    queryset = resultOcn.objects.all()
    queryset.delete()
    queryset = resultCgv.objects.all()
    queryset.delete()
    queryset = resultSAction.objects.all()
    queryset.delete()


def printOcn():
    print('ddd')
    print(Ocnmovies)

def save_count_ocn(movies):
    for movie in movies:
        resultOcn(ch=movie.ch, title=movie.title, date=movie.date, time=movie.time,count=movies.filter(title=movie.title).count()).save()

def save_count_cgv(movies):
    for movie in movies:
        resultCgv(ch=movie.ch, title=movie.title, date=movie.date, time=movie.time, count=movies.filter(title=movie.title).count()).save()

def save_count_SAction(movies):
    for movie in movies:
        resultSAction(ch=movie.ch, title=movie.title, date=movie.date, time=movie.time, count=movies.filter(title=movie.title).count()).save()




if __name__=='__main__':
    printOcn()
    save_count_ocn(Ocnmovies)
    save_count_cgv(Cgvmovies)
    save_count_SAction(SActionSchedule)