# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category_list',
            name='user',
        ),
        migrations.DeleteModel(
            name='Category_List',
        ),
    ]
