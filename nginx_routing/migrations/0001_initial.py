# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 04:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('domain_name', models.CharField(max_length=200)),
                ('disabled', models.CharField(max_length=1, null=True)),
                ('use_tenant', models.CharField(max_length=200)),
                ('marathon_app_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'nginx_apps',
            },
        ),
        migrations.CreateModel(
            name='AppTenantDB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=200)),
                ('port', models.CharField(max_length=200)),
                ('dialect', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('db_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'nginx_app_tenant_db',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('domain_name', models.CharField(max_length=200)),
                ('disabled', models.CharField(max_length=200, null=True)),
                ('app', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nginx_routing.App')),
            ],
            options={
                'db_table': 'nginx_domains',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('instance_id', models.CharField(max_length=200, unique=True)),
                ('instance_ip', models.CharField(max_length=200)),
                ('instance_port', models.CharField(max_length=9)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nginx_routing.App')),
            ],
            options={
                'db_table': 'nginx_groups',
            },
        ),
        migrations.AddField(
            model_name='domain',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nginx_routing.Group'),
        ),
        migrations.AddField(
            model_name='app',
            name='app_tenant_db',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nginx_routing.AppTenantDB'),
        ),
    ]
