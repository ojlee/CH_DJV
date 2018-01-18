from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=50, null=True)
    grade = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    genre = models.CharField(max_length=10, null=True)
    nation = models.CharField(max_length=10, null=True)
    premiere = models.DateField(null=True)
    director = models.CharField(max_length=20, null=True)
    actor = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title
