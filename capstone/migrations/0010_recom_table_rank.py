# Generated by Django 3.0.1 on 2020-04-14 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0009_auto_20200413_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='recom_table',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]
