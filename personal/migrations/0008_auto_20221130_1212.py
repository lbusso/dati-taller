# Generated by Django 3.1 on 2022-11-30 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0007_remove_personalfica_mail2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('dni', models.BigIntegerField(unique=True)),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
                ('es_docente', models.BooleanField(default=False)),
                ('es_nodo', models.BooleanField(default=False)),
                ('es_fica', models.BooleanField(default=False)),
                ('es_fcejs', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='PersonalFICA',
        ),
    ]
