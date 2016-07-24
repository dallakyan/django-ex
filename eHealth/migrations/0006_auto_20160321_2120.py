# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0005_auto_20160316_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searcher',
            name='password',
        ),
        migrations.RemoveField(
            model_name='searcher',
            name='username',
        ),
    ]
