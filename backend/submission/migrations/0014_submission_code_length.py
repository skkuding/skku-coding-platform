# Generated by Django 3.2.12 on 2022-02-10 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0013_auto_20211030_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='code_length',
            field=models.IntegerField(default=0),
        ),
    ]