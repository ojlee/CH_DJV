from django.contrib import admin

# Register your models here.
from .models import OcnSchedule
from .models import CgvSchedule
from .models import SActionSchedule
from .models import resultOcn
from .models import resultCgv
from .models import resultSAction



admin.site.register(OcnSchedule)
admin.site.register(CgvSchedule)
admin.site.register(SActionSchedule)
admin.site.register(resultOcn)
admin.site.register(resultCgv)
admin.site.register(resultSAction)