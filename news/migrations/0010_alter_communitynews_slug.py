# Generated by Django 4.2.2 on 2023-06-19 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_communitynews_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitynews',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
