# Generated by Django 2.1.1 on 2019-06-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20190623_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]