# Generated by Django 3.2.5 on 2021-12-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0003_migrate_languages_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysoptions',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sysoptions',
            name='value',
            field=models.JSONField(),
        ),
    ]