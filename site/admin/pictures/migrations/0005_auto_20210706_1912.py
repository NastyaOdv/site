# Generated by Django 3.2.4 on 2021-07-06 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0004_alter_artist_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='id_artist',
        ),
        migrations.AddField(
            model_name='picture',
            name='id_user',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
