# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0006_auto_20160321_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='searcher',
            name='username',
            field=models.CharField(default=b'user_name', unique=True, max_length=40),
            preserve_default=True,
        ),
    ]
