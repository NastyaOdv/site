# Generated by Django 3.2.4 on 2021-06-25 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='id_artist',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
