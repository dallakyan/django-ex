# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0002_auto_20160313_0039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_public', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=1000)),
                ('slug', models.SlugField()),
                ('user', models.ForeignKey(to='eHealth.Searcher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linkURL', models.URLField()),
                ('title', models.CharField(max_length=200)),
                ('visits', models.PositiveIntegerField(default=0)),
                ('summary', models.CharField(max_length=1000)),
                ('flesch_score', models.PositiveIntegerField()),
                ('polarity_score', models.PositiveIntegerField()),
                ('subjectivity_score', models.PositiveIntegerField()),
                ('category', models.ForeignKey(to='eHealth.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
