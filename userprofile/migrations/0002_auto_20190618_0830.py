# Generated by Django 2.1.1 on 2019-06-18 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone_umber',
            new_name='phone_number',
        ),
    ]
