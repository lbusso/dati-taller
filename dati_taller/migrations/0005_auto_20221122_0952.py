# Generated by Django 3.1 on 2022-11-22 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dati_taller', '0004_auto_20221117_0802'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinosDeReparacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('direccion', models.CharField(blank=True, max_length=150, verbose_name='Dirección')),
            ],
        ),
        migrations.AlterModelOptions(
            name='motivosordenesenaula',
            options={'verbose_name': 'Motivo de orden en aula', 'verbose_name_plural': 'Motivos de ordenes en aulas'},
        ),
        migrations.AddField(
            model_name='equipo',
            name='lugar_reparacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dati_taller.destinosdereparacion', verbose_name='Destino al que se envió a reparar'),
        ),
    ]