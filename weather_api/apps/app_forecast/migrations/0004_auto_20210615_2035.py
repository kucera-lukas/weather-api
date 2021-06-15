# Generated by Django 3.2.4 on 2021-06-15 18:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_forecast', '0003_alter_forecast_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='country_code',
            field=models.CharField(db_index=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='date',
            field=models.DateField(db_index=True, default=datetime.date.today, unique=True),
        ),
    ]