# Generated by Django 4.2.2 on 2023-06-19 09:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurednews',
            name='publishedDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='timestamp',
            name='creationDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
