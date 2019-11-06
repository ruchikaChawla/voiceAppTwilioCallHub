# Generated by Django 2.2.7 on 2019-11-06 09:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiceBroadcastApp', '0003_auto_20191106_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='call',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 15, 15, 40, 936036)),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 15, 15, 40, 935038)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 15, 15, 40, 934041)),
        ),
        migrations.AlterField(
            model_name='phonebook',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 15, 15, 40, 933044)),
        ),
    ]
