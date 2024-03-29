# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 20:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Existence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('date_time', models.DateTimeField(auto_now=True, verbose_name='Date and Time')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.Branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ExistenceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Folio Number')),
                ('date_time', models.DateTimeField(auto_now=True, verbose_name='Date and Time')),
                ('action', models.CharField(choices=[('altas', 'Altas'), ('bajas', 'Bajas'), ('baja_tras', 'baja_tras'), ('alta_tras', 'alta_tras')], max_length=255, verbose_name='Acci\xf3n')),
                ('printed', models.BooleanField(default=False, verbose_name='Enabled')),
                ('extra', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Extra')),
                ('details', models.TextField(blank=True, null=True, verbose_name='Details')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.Branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExistenceHistoryDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('existence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.ExistenceHistory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('comments', models.TextField(blank=True, max_length=1024, verbose_name='Comments')),
                ('adjusting', models.BooleanField(default=False, verbose_name='Adjusting')),
                ('branch', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='branches.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryAdjustment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('message', models.TextField(default=b'', verbose_name='Message')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('date_time', models.DateTimeField(auto_now=True, verbose_name='Date and Time')),
                ('inv', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Inventory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryFolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.PositiveIntegerField(verbose_name='Value')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(max_length=255, verbose_name='Status')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time')),
                ('branch_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_from', to='branches.Branch')),
                ('branch_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_to', to='branches.Branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTransferDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('product_transfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ProductTransfer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTransferHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True, verbose_name='Date and Time')),
                ('status_previous', models.TextField(max_length=255, verbose_name='Status Previous')),
                ('status_changed', models.TextField(max_length=255, verbose_name='Status Changed')),
                ('product_transfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ProductTransfer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='inventoryadjustment',
            name='inventory_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.InventoryEntry'),
        ),
    ]
