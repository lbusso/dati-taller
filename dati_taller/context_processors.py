from .models import *


def notificaciones(request):
    if (request.user.is_authenticated):
        if request.user.is_superuser:
            noti_taller = OrdenDeServicioEnTaller.objects.filter(estado='Pendiente')
            noti_domicilio = OrdenDeServicioADomicilio.objects.filter(estado='Pendiente')
            noti_aula = OrdenDeServicioEnAula.objects.filter(estado='Pendiente')
            noti_evento = Evento.objects.filter(terminado=False)

        else:
            noti_taller = OrdenDeServicioEnTaller.objects.filter(estado='Pendiente', tecnico=request.user)
            noti_domicilio = OrdenDeServicioADomicilio.objects.filter(estado='Pendiente', tecnico=request.user)
            noti_aula = OrdenDeServicioEnAula.objects.filter(estado='Pendiente', tecnico=request.user)
            noti_evento = Evento.objects.filter(terminado=False, tecnico=request.user)

        context = {
            'noti_taller': noti_taller,
            'noti_domicilio': noti_domicilio,
            'noti_aula': noti_aula,
            'noti_evento': noti_evento,
        }

        return context
    else:
        return {}



def recuento(request):
    if (request.user.is_authenticated):
        if request.user.is_superuser:
            orden_pendiente = OrdenDeServicioEnTaller.objects.exclude(estado='Terminado')
            orden_resueltas = OrdenDeServicioEnTaller.objects.all().filter(estado='Terminado')
            domicilio_pendiente = OrdenDeServicioADomicilio.objects.exclude(estado='Terminado')
            domicilio_resueltos = OrdenDeServicioADomicilio.objects.filter(estado='Terminado')
            aula_pendiente = OrdenDeServicioEnAula.objects.exclude(estado='Terminado')
            aula_resueltos = OrdenDeServicioEnAula.objects.filter(estado='Terminado')
            evento_pendiente = Evento.objects.filter(terminado=False)
            evento_resueltos = Evento.objects.filter(terminado=True)

        else:
            orden_pendiente = OrdenDeServicioEnTaller.objects.exclude(estado='Terminado',tecnico=request.user)
            orden_resueltas = OrdenDeServicioEnTaller.objects.filter(estado='Terminado')
            domicilio_pendiente = OrdenDeServicioADomicilio.objects.exclude(estado='Terminado',tecnico=request.user)
            domicilio_resueltos = OrdenDeServicioADomicilio.objects.filter(estado='Terminado')
            aula_pendiente = OrdenDeServicioEnAula.objects.exclude(estado='Terminado',tecnico=request.user)
            aula_resueltos = OrdenDeServicioEnAula.objects.filter(estado='Terminado')
            evento_pendiente = Evento.objects.filter(terminado=False,tecnico=request.user)
            evento_resueltos = Evento.objects.filter(terminado=True)

        context = {
            'card_orden': orden_pendiente,
            'card_orden_resuelto': orden_resueltas,
            'card_domicilio': domicilio_pendiente,
            'card_domicilio_resuelto': domicilio_resueltos,
            'card_aula': aula_pendiente,
            'card_aula_resuelto': aula_resueltos,
            'card_evento': evento_pendiente,
            'card_evento_resuelto': evento_resueltos
            }

        return context
    else:
        return {}
