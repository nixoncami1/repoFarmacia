# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-19 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appF', '0003_userprofile_contra'),
    ]

    operations = [
        migrations.CreateModel(
            name='farmacia_persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idfarmacia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appF.farmacia')),
                ('idpersona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appF.UserProfile')),
            ],
        ),
    ]
