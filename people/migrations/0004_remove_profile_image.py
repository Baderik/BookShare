# Generated by Django 3.0.8 on 2020-07-02 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20200701_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]