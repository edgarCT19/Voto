# Generated by Django 5.0.6 on 2024-06-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prep', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='total_votos',
            field=models.IntegerField(default=0),
        ),
    ]
