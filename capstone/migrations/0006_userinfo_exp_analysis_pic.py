# Generated by Django 3.0.1 on 2020-04-07 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0005_auto_20200331_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='exp_analysis_pic',
            field=models.ImageField(blank=True, null=True, upload_to='analysis_pics'),
        ),
    ]
