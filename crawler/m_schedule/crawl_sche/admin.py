from django.contrib import admin

# Register your models here.
from .models import OcnSchedule
from .models import CgvSchedule
from .models import SActionSchedule

admin.site.register(OcnSchedule)
admin.site.register(CgvSchedule)
admin.site.register(SActionSchedule)