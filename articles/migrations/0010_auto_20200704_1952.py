# Generated by Django 3.0.8 on 2020-07-04 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20200704_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='articles.Tag'),
        ),
    ]
