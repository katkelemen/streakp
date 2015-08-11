# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_credit(apps, schema_editor):
    Credit = apps.get_model("goals", "Credit")
    User = apps.get_model("auth", "User")
    for user in User.objects.all():
        if user.credit_set.all().count() == 0:
            Credit.objects.create(user=user, credit=1)

class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0008_achievement'),
    ]

    operations = [
        migrations.RunPython(add_credit),
    ]
