# Generated by Django 3.2.11 on 2022-02-02 16:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0004_alter_groupapplication_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', through='group.GroupMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
