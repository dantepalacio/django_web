# Generated by Django 4.1.6 on 2023-03-18 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_like_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.BooleanField(default=False, verbose_name='profile status'),
        ),
    ]
