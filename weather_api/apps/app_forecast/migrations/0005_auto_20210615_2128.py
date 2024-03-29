# Generated by Django 3.2.4 on 2021-06-15 19:28

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_forecast", "0004_auto_20210615_2035"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forecast",
            name="date",
            field=models.DateField(db_index=True, default=datetime.date.today),
        ),
        migrations.AddConstraint(
            model_name="forecast",
            constraint=models.UniqueConstraint(
                fields=("date", "country_code"),
                name="date and country_code pair",
            ),
        ),
    ]
