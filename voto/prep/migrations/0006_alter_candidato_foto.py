# Generated by Django 5.0.6 on 2024-06-09 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prep', '0005_roles_tipocasilla_remove_funcionario_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='foto',
            field=models.ImageField(null=True, upload_to='candidatos_fotos/'),
        ),
    ]
