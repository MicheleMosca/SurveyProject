# Generated by Django 3.2.9 on 2022-05-11 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='image_collection',
            unique_together={('image', 'survey_collection')},
        ),
    ]