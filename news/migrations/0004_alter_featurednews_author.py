# Generated by Django 4.2.2 on 2023-06-19 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_rename_imageurl_featurednews_image_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurednews',
            name='author',
            field=models.CharField(blank=True, default='Anonymous', max_length=50, null=True),
        ),
    ]
