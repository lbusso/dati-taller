# Generated by Django 3.1 on 2022-10-17 13:40

import dati_taller.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fontawesome_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellido', models.CharField(max_length=150)),
                ('nombre', models.CharField(max_length=150)),
                ('box', models.CharField(blank=True, max_length=150, null=True)),
                ('interno', models.IntegerField(blank=True, null=True)),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='ElementosParaEventos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Elementos para eventos',
                'verbose_name_plural': 'Elementos para eventos',
            },
        ),
        migrations.CreateModel(
            name='EquipamientoAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('icon', fontawesome_5.fields.IconField(blank=True, max_length=60)),
            ],
            options={
                'verbose_name': 'Equipamiento para Aulas',
                'verbose_name_plural': 'Equipamiento para Aulas',
            },
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveBigIntegerField(unique=True, verbose_name='Codigo de Barras')),
                ('caracteristicas', models.TextField(blank=True, null=True, verbose_name='Caracteristicas del equipo')),
                ('en_taller', models.BooleanField(default=False, verbose_name='El Equipo esta en el taller')),
                ('en_reparacion', models.BooleanField(default=False, verbose_name='Se envi?? a reparar')),
            ],
            options={
                'verbose_name_plural': 'Equipos',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('hora_fin', models.TimeField(default='00:00', verbose_name='Horario tentantivo de finalizaci??n')),
                ('terminado', models.BooleanField(default=False)),
                ('aula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.aula')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.cliente')),
                ('lista_elementos', models.ManyToManyField(to='dati_taller.ElementosParaEventos')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MotivosOrdenesEnDomicilio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Motivo de orden en domicilio',
                'verbose_name_plural': 'Motivos de ordenes en domicilio',
            },
        ),
        migrations.CreateModel(
            name='MotivosOrdenesEnTaller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Motivo de orden en taller',
                'verbose_name_plural': 'Motivos de ordenes en taller',
            },
        ),
        migrations.CreateModel(
            name='Ordenes_old',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True)),
                ('cliente', models.CharField(max_length=250, null=True)),
                ('problema', models.TextField(null=True)),
                ('observacion', models.TextField(null=True)),
                ('tecnico', models.CharField(max_length=250, null=True)),
                ('fecha_entega', models.DateField(null=True)),
                ('equipo', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Orden Vieja de servicio',
                'verbose_name_plural': 'Ordenes viejas de servicio',
            },
        ),
        migrations.CreateModel(
            name='TipoDeEquipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Tipo de Equipo',
                'verbose_name_plural': 'Tipos de Equipo',
            },
        ),
        migrations.CreateModel(
            name='TipoDeEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': ' Tipo de Evento',
                'verbose_name_plural': 'Tipos de Evento',
            },
        ),
        migrations.CreateModel(
            name='ProductoParaPrestar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.categoria')),
            ],
            options={
                'verbose_name': 'Producto para prestar',
                'verbose_name_plural': 'Productos para prestar',
            },
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_prestamo', models.DateTimeField(auto_now_add=True)),
                ('devuelto', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.cliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.productoparaprestar')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenDeServicioEnTaller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(default=dati_taller.models.get_ticket, max_length=11)),
                ('observaciones', models.CharField(blank=True, max_length=250)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
                ('fecha_entrega', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'PENDIENTE'), ('En Proceso', 'EN PROCESO'), ('Terminado', 'TERMINADO')], default='Pendiente', max_length=250)),
                ('entregado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.cliente')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.equipo')),
                ('motivo_ingreso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dati_taller.motivosordenesentaller')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Orden de servicio en taller',
                'verbose_name_plural': 'Ordenes de servicio en taller',
            },
        ),
        migrations.CreateModel(
            name='OrdenDeServicioEnAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(default=dati_taller.models.get_ticket, max_length=11)),
                ('motivo', models.CharField(max_length=250)),
                ('estado', models.CharField(blank=True, choices=[('Pendiente', 'PENDIENTE'), ('En Proceso', 'EN PROCESO'), ('Terminado', 'TERMINADO')], default='Pendiente', max_length=100, null=True)),
                ('fecha', models.DateField(auto_now=True)),
                ('aula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.aula')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Orden de Servicio en Aula',
                'verbose_name_plural': 'Ordenes de servicio en Aulas',
            },
        ),
        migrations.CreateModel(
            name='OrdenDeServicioADomicilio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(default=dati_taller.models.get_ticket, max_length=11)),
                ('observaciones', models.CharField(blank=True, max_length=200)),
                ('estado', models.CharField(choices=[('Pendiente', 'PENDIENTE'), ('En Proceso', 'EN PROCESO'), ('Terminado', 'TERMINADO')], default='Pendiente', max_length=150)),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('fecha_realizado', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.cliente')),
                ('motivo_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.motivosordenesendomicilio')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Orden de Servicio a domicilio',
                'verbose_name_plural': 'Ordenes de Servicio a Domicilio',
                'permissions': [('is_tecnico', 'Es Personal tecnico del cdc')],
            },
        ),
        migrations.CreateModel(
            name='InformeTaller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informe', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dati_taller.ordendeservicioentaller')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Informes_old',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True)),
                ('tecnico', models.CharField(max_length=250, null=True)),
                ('informe', models.TextField(null=True)),
                ('orden', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dati_taller.ordenes_old')),
            ],
        ),
        migrations.CreateModel(
            name='InformeEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informe', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dati_taller.evento')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InformeDomicilio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informe', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dati_taller.ordendeservicioadomicilio')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InformeAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informe', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dati_taller.ordendeservicioenaula')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='equipo',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dati_taller.tipodeequipo'),
        ),
        migrations.AddField(
            model_name='aula',
            name='equipamiento',
            field=models.ManyToManyField(to='dati_taller.EquipamientoAula'),
        ),
    ]
