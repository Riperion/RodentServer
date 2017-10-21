# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 22:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RatSighting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('location_type', models.TextField()),
                ('zip_code', models.IntegerField()),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=100)),
                ('borough', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
    ]