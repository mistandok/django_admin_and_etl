# Generated by Django 3.2 on 2022-12-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['modified'], name='film_work_modified_idx'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['modified'], name='genre_modified_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['modified'], name='person_modified_idx'),
        ),
    ]
