# Generated by Django 3.2.4 on 2021-06-15 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_forecast', '0002_rename_result_forecast_forecast'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='date',
            field=models.DateField(auto_now_add=True, unique=True),
        ),
    ]
