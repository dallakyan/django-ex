# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0008_remove_searcher_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searcher',
            name='age',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
