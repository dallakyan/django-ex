# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eHealth', '0004_saved_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saved_page',
            name='link',
        ),
        migrations.RemoveField(
            model_name='saved_page',
            name='user',
        ),
        migrations.DeleteModel(
            name='Saved_Page',
        ),
        migrations.AddField(
            model_name='page',
            name='is_public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
