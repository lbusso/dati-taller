# Generated by Django 3.1 on 2022-11-28 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_auto_20221108_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalFICA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('dni', models.BigIntegerField(unique=True)),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
                ('mail2', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Alternativo')),
                ('es_docente', models.BooleanField(default=False)),
                ('es_nodo', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='departamentofcejs',
            options={'verbose_name_plural': 'Departamentos FCEJS'},
        ),
        migrations.AlterModelOptions(
            name='personalfcejs',
            options={'verbose_name_plural': 'Personal FCEJS'},
        ),
    ]
