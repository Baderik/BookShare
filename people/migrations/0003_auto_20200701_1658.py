# Generated by Django 3.0.7 on 2020-07-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_profile_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(default=None, max_length=18, null=True),
        ),
    ]