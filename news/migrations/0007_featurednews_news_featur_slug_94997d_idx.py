# Generated by Django 4.2.2 on 2023-06-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_featurednews_slug_alter_featurednews_title'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='featurednews',
            index=models.Index(fields=['slug'], name='news_featur_slug_94997d_idx'),
        ),
    ]