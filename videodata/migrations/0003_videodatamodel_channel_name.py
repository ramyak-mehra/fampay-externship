# Generated by Django 4.0 on 2021-12-18 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videodata', '0002_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='videodatamodel',
            name='channel_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
