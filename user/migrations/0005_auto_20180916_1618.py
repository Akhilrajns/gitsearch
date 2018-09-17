# Generated by Django 2.1.1 on 2018-09-16 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_githubuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubuser',
            name='company',
            field=models.CharField(blank=True, max_length=255, verbose_name='Company'),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='location',
            field=models.CharField(blank=True, max_length=255, verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name'),
        ),
    ]