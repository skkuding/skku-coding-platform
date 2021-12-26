# Generated by Django 3.2.5 on 2021-12-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20190326_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acmcontestrank',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='acmcontestrank',
            name='submission_info',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='contest',
            name='allowed_ip_ranges',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='contest',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='contestannouncement',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='oicontestrank',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='oicontestrank',
            name='submission_info',
            field=models.JSONField(default=dict),
        ),
    ]
