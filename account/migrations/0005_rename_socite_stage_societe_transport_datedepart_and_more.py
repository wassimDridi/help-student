# Generated by Django 5.0.2 on 2024-04-20 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_post_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stage',
            old_name='socite',
            new_name='societe',
        ),
        migrations.AddField(
            model_name='transport',
            name='datedepart',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='transport',
            name='heureDep',
            field=models.IntegerField(default=12),
        ),
    ]
