# Generated by Django 3.2.9 on 2022-03-08 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='survey',
            new_name='survey_collection',
        ),
    ]
