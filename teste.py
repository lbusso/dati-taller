from dati_taller.models import Evento

evento1 =Evento.objects.get(id=29)
evento2 =Evento.objects.get(id=30)

print(evento1.hora)
print(evento2.hora)