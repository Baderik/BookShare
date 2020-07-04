# Generated by Django 3.0.8 on 2020-07-04 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='articles.Tag'),
        ),
    ]
