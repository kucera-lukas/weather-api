# Generated by Django 3.2.4 on 2021-06-15 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_forecast", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="forecast",
            old_name="result",
            new_name="forecast",
        ),
    ]