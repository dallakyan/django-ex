# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0003_category_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saved_Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_public', models.BooleanField(default=False)),
                ('link', models.OneToOneField(to='eHealth.Page')),
                ('user', models.ForeignKey(to='eHealth.Searcher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
