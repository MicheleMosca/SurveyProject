# Generated by Django 3.2.9 on 2022-05-09 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=200)),
                ('name', models.CharField(default='', max_length=200)),
            ],
            options={
                'unique_together': {('name', 'path')},
            },
        ),
        migrations.CreateModel(
            name='Survey_Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey_collection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image_Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transformation', models.CharField(max_length=200)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.image')),
                ('survey_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey_collection')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('survey_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey_collection')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.choice')),
                ('image_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.image_collection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('image_collection', 'user')},
            },
        ),
    ]
