# Generated by Django 3.1 on 2020-09-21 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listingid',
        ),
    ]
