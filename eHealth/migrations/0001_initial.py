# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Searcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=40)),
                ('password', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=75)),
                ('name', models.CharField(max_length=1000)),
                ('surname', models.CharField(max_length=1000)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=6, choices=[(b'Other', b'Other'), (b'Male', b'Male'), (b'Female', b'Female')])),
                ('searcher', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='category_list',
            name='user',
            field=models.ForeignKey(to='eHealth.Searcher'),
            preserve_default=True,
        ),
    ]
