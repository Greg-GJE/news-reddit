# Generated by Django 4.2.2 on 2023-09-13 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_alter_communitynews_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurednews',
            name='author',
            field=models.CharField(blank=True, default='Anonymous', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='featurednews',
            name='description',
            field=models.TextField(),
        ),
    ]
