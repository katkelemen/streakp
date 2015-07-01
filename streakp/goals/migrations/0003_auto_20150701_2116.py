# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_goal_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='goal',
            unique_together=set([('user', 'name')]),
        ),
    ]
