# Generated by Django 3.0.7 on 2020-07-01 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='facebook',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='odnoklassniki',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='phone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='telegram',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='twitter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='viber',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='vk',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='whatsapp',
            field=models.BooleanField(default=False),
        ),
    ]
