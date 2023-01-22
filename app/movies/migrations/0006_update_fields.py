# Generated by Django 3.2 on 2022-12-30 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_renamed_fields_for_data_migration_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='filmworks',
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.Person'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work_id', 'person_id'], name='film_work_person_idx'),
        ),
    ]