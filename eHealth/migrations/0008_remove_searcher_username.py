# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0007_searcher_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searcher',
            name='username',
        ),
    ]
