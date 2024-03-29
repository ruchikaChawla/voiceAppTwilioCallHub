# Generated by Django 2.2.7 on 2019-11-06 09:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(default='admin', max_length=255)),
                ('name', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('created_date', models.DateTimeField(default=datetime.datetime(2019, 11, 6, 14, 47, 18, 979792))),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(default='admin', max_length=255)),
                ('first_name', models.CharField(default='', max_length=255)),
                ('last_name', models.CharField(default='', max_length=255)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2019, 11, 6, 14, 47, 18, 979792))),
                ('phone_number', models.IntegerField(unique=True)),
                ('phone_book', models.ManyToManyField(to='voiceBroadcastApp.PhoneBook')),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(default='admin', max_length=255)),
                ('name', models.CharField(default='', max_length=255)),
                ('text_speech', models.TextField(default='')),
                ('status', models.CharField(choices=[('created', 'created'), ('started', 'started'), ('completed', 'completed')], default='created', max_length=20)),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2019, 11, 6, 14, 47, 18, 981787))),
                ('started_date', models.DateTimeField(blank=True, null=True)),
                ('phone_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voiceBroadcastApp.PhoneBook')),
            ],
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(default='admin', max_length=255)),
                ('call_sid', models.CharField(default='', max_length=255, unique=True)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2019, 11, 6, 14, 47, 18, 981787))),
                ('duration', models.IntegerField()),
                ('caller_id', models.CharField(default='', max_length=255)),
                ('cost', models.IntegerField()),
                ('campaign_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voiceBroadcastApp.Campaign')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voiceBroadcastApp.Contact')),
            ],
        ),
    ]
