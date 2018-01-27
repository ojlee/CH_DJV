from django.db import models

# Create your models here.

class OcnSchedule(models.Model):
    # no = models.IntegerField()
    ch = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField()
    def __str__(self):
        return self.title

class CgvSchedule(models.Model):
    # no = models.IntegerField()
    ch = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField()
    def __str__(self):
        return self.title

class SActionSchedule(models.Model):
    # no = models.IntegerField()
    ch = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField()
    def __str__(self):
        return self.title
    
class resultOcn(models.Model):
    ch = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField()
    count = models.IntegerField()
    def __str__(self):
        return self.title

class resultCgv(models.Model):
    ch = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField()
    count = models.IntegerField()
    def __str__(self):
        return self.title

class resultSAction(models.Model):
    ch = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField()
    count = models.IntegerField()

    def __str__(self):
        return self.title


