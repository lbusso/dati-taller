import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from fontawesome_5.fields import IconField

from personal.models import Personal


class Cliente(models.Model):
    apellido = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    box = models.CharField(max_length=150, blank=True, null=True)
    interno = models.IntegerField(blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.apellido + ' ' + self.nombre

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class EquipamientoAula(models.Model):
    nombre = models.CharField(max_length=200)
    icon = IconField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Equipamiento para Aulas'
        verbose_name_plural = 'Equipamiento para Aulas'


class Aula(models.Model):
    nombre = models.CharField(max_length=200)
    equipamiento = models.ManyToManyField(EquipamientoAula)

    def __str__(self):
        return self.nombre


'---------------------------------------------------------------------------------------------------------- '


# Taller CDC modelos relacionados con el taller
class MotivosOrdenesEnTaller(models.Model):
    motivo = models.CharField(max_length=200)

    def __str__(self):
        return self.motivo

    class Meta:
        verbose_name = 'Motivo de orden en taller'
        verbose_name_plural = 'Motivos de ordenes en taller'

class SolucionAMotivoOrdenEnTaller(models.Model):
    motivo = models.ForeignKey(MotivosOrdenesEnTaller, on_delete=models.CASCADE, verbose_name='Motivo relacionado con la solucion')
    solucion = models.CharField(max_length=150)

    def __str__(self):
        return self.solucion

class TipoDeEquipo(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de Equipo'
        verbose_name_plural = 'Tipos de Equipo'

class DestinosDeReparacion(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    tipo = models.ForeignKey(TipoDeEquipo, on_delete=models.CASCADE)
    codigo = models.PositiveBigIntegerField(verbose_name='Codigo de Barras', unique=True)
    caracteristicas = models.TextField(blank=True, null=True, verbose_name='Caracteristicas del equipo')
    en_taller = models.BooleanField(default=False, verbose_name='El Equipo esta en el taller')
    en_reparacion = models.BooleanField(default=False, verbose_name='Se envió a reparar')
    lugar_reparacion = models.ForeignKey(DestinosDeReparacion, on_delete= models.CASCADE, blank=True, null=True, verbose_name='Destino al que se envió a reparar')


    def __str__(self):
        return str(self.codigo)

    class Meta:
        verbose_name_plural = 'Equipos'


def get_ticket():
    ticket = str(uuid.uuid4())
    return ticket[:10]


class OrdenDeServicioEnTaller(models.Model):
    estados = [
        ('Pendiente', 'PENDIENTE'),
        ('En Proceso', 'EN PROCESO'),
        ('Terminado', 'TERMINADO'),
    ]

    ticket = models.CharField(max_length=11, default=get_ticket)
    # create_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    cliente = models.ForeignKey(Personal, on_delete=models.CASCADE, verbose_name='Cliente')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    motivo_ingreso = models.ForeignKey(MotivosOrdenesEnTaller, on_delete=models.CASCADE, blank=True, null=True)
    observaciones = models.CharField(max_length=250, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(auto_now=True)
    solucion_implementada = models.ForeignKey(SolucionAMotivoOrdenEnTaller, on_delete=models.CASCADE, verbose_name='Solucion Implementada', blank=True, null=True)
    estado = models.CharField(max_length=250, choices=estados, default='Pendiente')
    entregado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ticket)

    class Meta:
        verbose_name_plural = 'Ordenes de servicio en taller'
        verbose_name = 'Orden de servicio en taller'


class InformeTaller(models.Model):
    orden = models.ForeignKey(OrdenDeServicioEnTaller, on_delete=models.CASCADE, blank=True, null=True)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    informe = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orden)


# Ordenes de servicio a domicilio

class MotivosOrdenesEnDomicilio(models.Model):
    motivo = models.CharField(max_length=200)
    def __str__(self):
        return self.motivo
    class Meta:
        verbose_name = 'Motivo de orden en domicilio'
        verbose_name_plural = 'Motivos de ordenes en domicilio'

class SolucionAMotivoOrdenEnDomicilio(models.Model):
    motivo = models.ForeignKey(MotivosOrdenesEnDomicilio, on_delete=models.CASCADE, verbose_name='Motivo relacionado con la solucion')
    solucion = models.CharField(max_length=150)

    def __str__(self):
        return self.solucion

class OrdenDeServicioADomicilio(models.Model):
    def image_path(instance, filename):
        return 'images/{}/{}'.format(instance.motivo_servicio, filename)
    estados = [
        ('Pendiente', 'PENDIENTE'),
        ('En Proceso', 'EN PROCESO'),
        ('Terminado', 'TERMINADO'),
    ]
    ticket = models.CharField(max_length=11, default=get_ticket)
    cliente = models.ForeignKey(Personal, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    motivo_servicio = models.ForeignKey(MotivosOrdenesEnDomicilio, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=200, blank=True, )
    imagen = models.ImageField(upload_to=image_path, blank=True, null=True, verbose_name= 'Imagen de referencia')
    estado = models.CharField(max_length=150, choices=estados, default='Pendiente')
    solucion_implementada = models.ForeignKey(SolucionAMotivoOrdenEnDomicilio, on_delete=models.CASCADE, verbose_name='Solucion Implementada', blank=True, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_realizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ticket)

    class Meta:
        permissions = [
            ('is_tecnico', 'Es Personal tecnico del cdc')
        ]
        verbose_name = 'Orden de Servicio a domicilio'
        verbose_name_plural = 'Ordenes de Servicio a Domicilio'


class InformeDomicilio(models.Model):
    orden = models.ForeignKey(OrdenDeServicioADomicilio, on_delete=models.CASCADE, blank=True, null=True)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    informe = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orden)


# Ordenes de servicio en Aulas

class MotivosOrdenesEnAula(models.Model):
    motivo = models.CharField(max_length=200)
    def __str__(self):
        return self.motivo
    class Meta:
        verbose_name = 'Motivo de orden en aula'
        verbose_name_plural = 'Motivos de ordenes en aulas'

class SolucionAMotivoOrdenEnAula(models.Model):
    motivo = models.ForeignKey(MotivosOrdenesEnAula, on_delete=models.CASCADE, verbose_name='Motivo relacionado con la solucion en Aula')
    solucion = models.CharField(max_length=150)

    def __str__(self):
        return self.solucion
class OrdenDeServicioEnAula(models.Model):
    estados = [
        ('Pendiente', 'PENDIENTE'),
        ('En Proceso', 'EN PROCESO'),
        ('Terminado', 'TERMINADO'),
    ]
    ticket = models.CharField(max_length=11, default=get_ticket)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    motivo = models.ForeignKey(MotivosOrdenesEnAula, on_delete=models.CASCADE, verbose_name='Motivo de la visita')
    estado = models.CharField(max_length=100, choices=estados, blank=True, null=True, default='Pendiente')
    solucion_implementada = models.ForeignKey(SolucionAMotivoOrdenEnAula, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.aula)

    class Meta:
        verbose_name = 'Orden de Servicio en Aula'
        verbose_name_plural = 'Ordenes de servicio en Aulas'


class InformeAula(models.Model):
    orden = models.ForeignKey(OrdenDeServicioEnAula, on_delete=models.CASCADE, blank=True, null=True)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    informe = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orden)


# Eventos

class TipoDeEvento(models.Model):
    nombre = models.CharField(max_length=250, )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = ' Tipo de Evento'
        verbose_name_plural = 'Tipos de Evento'


class ElementosParaEventos(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Elementos para eventos'
        verbose_name_plural = 'Elementos para eventos'


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    cliente = models.ForeignKey(Personal, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    hora_fin = models.TimeField(verbose_name='Horario tentantivo de finalización', default='00:00')
    lista_elementos = models.ManyToManyField(ElementosParaEventos)
    terminado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.titulo)


class InformeEvento(models.Model):
    orden = models.ForeignKey(Evento, on_delete=models.CASCADE, blank=True, null=True)
    tecnico = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    informe = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orden)


'-----------------------------------------------------------------------------------------'


# Informes del sistema taller viejo
class Ordenes_old(models.Model):
    fecha = models.DateField(null=True)
    cliente = models.CharField(max_length=250, null=True)
    problema = models.TextField(null=True)
    observacion = models.TextField(null=True)
    tecnico = models.CharField(max_length=250, null=True)
    fecha_entega = models.DateField(null=True)
    equipo = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.cliente

    class Meta:
        verbose_name = "Orden Vieja de servicio"
        verbose_name_plural = "Ordenes viejas de servicio"


class Informes_old(models.Model):
    fecha = models.DateField(null=True)
    orden = models.ForeignKey(Ordenes_old, on_delete=models.CASCADE, null=True)
    tecnico = models.CharField(max_length=250, null=True)
    informe = models.TextField(null=True)


'-----------------------------------------------------------------------------------------------------'


# Sistema de prestamos e inventario

class Categoria(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre


class ProductoParaPrestar(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, )
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Producto para prestar'
        verbose_name_plural = 'Productos para prestar'


class Prestamo(models.Model):
    cliente = models.ForeignKey(Personal, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(ProductoParaPrestar, on_delete=models.CASCADE)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return self.cliente
