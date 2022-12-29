# Generated by Django 3.1 on 2022-11-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargopersonafcejs',
            options={'verbose_name': 'Cargo de cada persona', 'verbose_name_plural': 'Cargos de cada persona'},
        ),
        migrations.AddField(
            model_name='personalfcejs',
            name='es_docente',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personalfcejs',
            name='es_nodo',
            field=models.BooleanField(default=False),
        ),
    ]