# Generated by Django 4.2.2 on 2023-06-19 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_featurednews_publisheddate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='featurednews',
            old_name='imageUrl',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='featurednews',
            old_name='publishedDate',
            new_name='published_date',
        ),
    ]
