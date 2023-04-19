# Generated by Django 4.1.6 on 2023-04-18 17:57

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_arcticle_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='arcticle',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
    ]
