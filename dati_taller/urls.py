from django.urls import path
from .views import *
urlpatterns = [

#URL CLIENTES
    path('clientes/modal/', CrearCLienteModal.as_view(), name='cliente_create_modal'),
    path('clientes/create/', CreateClient.as_view(), name='cliente_create'),
    path('clientes/list/', ClienteList.as_view(), name='cliente_list'),
    path('clientes/edit/<int:pk>', ClienteEdit.as_view(), name='cliente_edit'),

    path('clientes/modal/aula', CrearAulaModal.as_view(), name='aula_create_modal'),
    path('clientes/aula/create', AulaCreate.as_view(), name='aula_create'),
    path('clientes/aula/list', AulaList.as_view(), name='aula_list'),
    path('clientes/aula/edit/<int:pk>', AulaEdit.as_view(), name='aula_edit'),

#URLS DE TALLER
    #Equipos
    path('equipo/create', EquipoCreate.as_view(), name='equipo_create'),
    path('equipo/create/modal/', CrearEquipoModal.as_view(), name='equipo_create_modal'),
    path('equipo/edit/<int:pk>', EquipoEdit.as_view(), name='equipo_edit'),
    path('equipo/list', EquipoList.as_view(), name='equipo_list'),
    path('equipo/result', OrdenResult.as_view(), name='equipo_result'),

    #Ordenes de servicio en taller
    path('orden/list', ordenesEntaller, name='orden_list'),
    path('orden/new', ordenTallerCreate, name='orden_create'),
    path('orden/detail/<int:pk>/', ordenTallerDetail, name='orden_detail'),
    path('orden/informe/<int:pk>/', informeTaller, name='orden_informe'),
    path('orden/transferir/<int:pk>/', transferirOrden, name='orden_transferir'),
    path('orden/enviar_reparacion/<int:pk>/', enviarAReparar, name='orden_enviar_reparar'),
    path('orden/devolver_de_reparar/<int:pk>/', volverDeReparar, name='orden_devolver_reparar'),
    path('orden/terminar/<int:pk>/', terminarOrden, name='orden_terminar'),
    path('orden/entregar/<int:pk>/', EntregarOrden, name='orden_entregar'),
    path('alerta-de-informe/', RealizarInforme.as_view(), name='realizar_informe'),

    #Ordenes a domicilio
    path('orden/domicilio/list/', domicilioList, name='domicilio_list'),
    path('orden/domicilio/new/', DomicilioCreate.as_view(), name='domicilio_create'),
    path('orden/domicilio/detail/<int:pk>/', ordenDomicilioDetail, name='domicilio_detail'),
    path('orden/domicilio/informe/<int:pk>/', informeDomicilio, name='domicilio_informe'),
    path('orden/domicilio/transferir/<int:pk>/', transferirDomicilio, name='domicilio_transferir'),
    path('orden/domicilio/terminar/<int:pk>/', terminarOrdenDomicilio, name='domicilio_terminar'),

    # Servicios en Aula
    path('orden/aula/new/', OrdenAulaCreate.as_view(), name='servicio_aula_create'),
    path('orden/aula/list/', ordenAulaList, name='servicio_aula_list'),
    path('orden/aula/detail/<int:pk>/', ordenAulaDetail, name='servicio_aula_detail'),
    path('orden/aula/informe/<int:pk>/', informeAula, name='servicio_aula_informe'),
    path('orden/aula/transferir/<int:pk>/', transferirOrdenAula, name='servicio_aula_transferir'),
    path('orden/aula/terminar/<int:pk>/', terminarOrdenAula, name='servicio_aula_terminar'),

    # Servicios Eventos

    path('orden/evento/new/', evento_create, name='evento_create'),
    path('orden/evento/edit/<int:pk>', EventoEdit.as_view(), name='evento_edit'),
    path('orden/evento/list/', ordenEventoList, name='evento_list'),
    path('orden/evento/list/hoy', ordenEventoListHoy, name='evento_list_hoy'),
    path('orden/evento/detail/<int:pk>/', ordenEventoDetail, name='evento_detail'),
    path('orden/evento/terminar/<int:pk>/', terminarEvento, name='evento_terminar'),
    path('orden/evento/transferir/<int:pk>/', transferirEvento, name='evento_transferir'),

    #search sistema viejo
    path('sistema-old/list/', OldOrdenesList.as_view(), name='old_orden_list'),
    path('sistema-old/detail/<int:pk>/', old_orden_detail, name='old_orden_detail'),
    path('sistema-old/search/cliente/', SearchClientResult.as_view(), name='old_client_result'),
    path('sistema-old/search/equipo/', SearchEquipoResult.as_view(), name='old_equipo_result'),

    #Sistema de prestamos
    path('create/', ProductoParaPrestarCreate.as_view(), name='prd_prestar_create'),
    path('list/', ProductoParaPrestarList.as_view(), name='prd_prestar_list'),

    #Prestamos
    path('prestamo/list', prestamo_list, name='prestamo_list'),
    path('prestamo/create', prestamoCreate, name='prestamo_create'),
    path('prestamo/devolver/<int:pk>', prestamo_devolver, name='prestamo_devolver'),
]