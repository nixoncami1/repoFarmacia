# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-20 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appF', '0005_farmacia_idpersona'),
    ]

    operations = [
        migrations.AddField(
            model_name='enfermedad',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='farmacia_medicamento',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='farmacia_persona',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='medicamento_enfermedad',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='persona_enfermedad',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]