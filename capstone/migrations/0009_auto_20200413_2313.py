# Generated by Django 3.0.1 on 2020-04-14 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0008_recom_table_match_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='recom_table',
            name='company_rating',
            field=models.FloatField(default=0, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recom_table',
            name='job_age',
            field=models.IntegerField(default=0),
        ),
    ]
