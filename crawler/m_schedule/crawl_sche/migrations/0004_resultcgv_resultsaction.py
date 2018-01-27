# Generated by Django 2.0.1 on 2018-01-27 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl_sche', '0003_resultocn'),
    ]

    operations = [
        migrations.CreateModel(
            name='resultCgv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ch', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='resultSAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ch', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('count', models.IntegerField()),
            ],
        ),
    ]
