# Generated by Django 3.0.8 on 2020-07-04 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_quote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
    ]
