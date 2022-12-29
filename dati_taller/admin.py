from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class InformesOldInline(admin.TabularInline):
    model = Informes_old
    extra = 1

class Ordenes_oldResourse(resources.ModelResource):
    class Meta:
        model = Ordenes_old

class Ordenes_oldAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    list_display = ['cliente', 'equipo', 'fecha', 'problema', 'observacion', 'tecnico']
    inlines = [InformesOldInline]


class Informes_oldResourse(resources.ModelResource):
    class Meta:
        model = Informes_old

class Informes_oldAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    list_display = [ 'orden', 'tecnico', 'fecha',]

class ClientResourse(resources.ModelResource):
    class Meta:
        model = Cliente
class ClienteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['apellido','nombre', 'box', 'interno', 'mail']
    search_fields = ['apellido', 'nombre']


class EquipamientoAulaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icon']

class EquipoResourse(resources.ModelResource):
    class Meta:
        model = Equipo
class EquipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['tipo', 'codigo', 'en_reparacion']


class InformesTallerInlines(admin.TabularInline):
    model = InformeTaller
    extra = 1


class OrdenDeServicioEnTallerAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'cliente', 'tecnico', 'fecha_ingreso', 'estado']
    inlines = [InformesTallerInlines]

class InformesDomicilioInlines(admin.TabularInline):
    model = InformeDomicilio
    extra = 1

class OrdenDeServicioADomicilioAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'tecnico',]
    inlines = [InformesDomicilioInlines]


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Aula)
admin.site.register(EquipamientoAula, EquipamientoAulaAdmin)

admin.site.register(TipoDeEquipo)
admin.site.register(DestinosDeReparacion)
admin.site.register(Equipo, EquipoAdmin)

admin.site.register(MotivosOrdenesEnTaller)
admin.site.register(SolucionAMotivoOrdenEnTaller)
admin.site.register(OrdenDeServicioEnTaller, OrdenDeServicioEnTallerAdmin)

admin.site.register(MotivosOrdenesEnDomicilio)
admin.site.register(SolucionAMotivoOrdenEnDomicilio)
admin.site.register(OrdenDeServicioADomicilio, OrdenDeServicioADomicilioAdmin)

admin.site.register(OrdenDeServicioEnAula)
admin.site.register(MotivosOrdenesEnAula)
admin.site.register(SolucionAMotivoOrdenEnAula)


admin.site.register(Evento)
admin.site.register(ElementosParaEventos)

admin.site.register(ProductoParaPrestar)
admin.site.register(Prestamo)
admin.site.register(Categoria)
