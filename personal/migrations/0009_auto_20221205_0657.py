# Generated by Django 3.1 on 2022-12-05 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0008_auto_20221130_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='box',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='personal',
            name='interno',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
