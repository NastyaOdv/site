# Generated by Django 3.2.5 on 2021-07-09 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='likes.post'),
        ),
    ]
