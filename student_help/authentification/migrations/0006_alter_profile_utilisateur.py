# Generated by Django 5.0.3 on 2024-03-19 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0005_profile_utilisateur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='utilisateur',
            field=models.IntegerField(default=0),
        ),
    ]
