# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 20:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=512, verbose_name='Last Name')),
                ('phonenumber', models.CharField(blank=True, max_length=512, null=True, validators=[django.core.validators.RegexValidator(b'[0-9]{3}\\-?[0-9]{3}\\-?[0-9]{4}', b'Format: 834-117-1086', b'phone_format_error')], verbose_name='Phone Number')),
                ('address', models.TextField(blank=True, max_length=1024, verbose_name='Address')),
                ('id_type', models.CharField(blank=True, choices=[(b'IFE', b'IFE (Credencial de Elector'), (b'LICENCIA', b'Licencia de conducir'), (b'PASAPORTE', b'Pasaporte'), (b'OTRO', b'Otro')], default=b'IFE', max_length=50, verbose_name='ID Type')),
                ('id_number', models.CharField(blank=True, max_length=255, verbose_name='Identification Number')),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='Correo electr\xf3nico')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
            },
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together=set([('first_name', 'last_name', 'phonenumber', 'email')]),
        ),
    ]
