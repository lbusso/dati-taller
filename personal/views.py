from django.shortcuts import render
from .models import Personal
from django.views.generic import ListView



"""
def createPersonaFica(request):
    docentes_fica = PersonalFCEJS.objects.all().distinct('dni')


    for p in docentes_fica:
        nombres = p.nombre.split(' ')
        apellido = nombres[0]
        if len(nombres)>= 3:
            nombre= nombres[1]+ ' ' + nombres[2]
        else:
            nombre = nombres[1]
        dni = p.dni
        mail = p.mail
        es_docente=  p.es_docente
        es_nodo=  p.es_nodo
        es_fcejs=  True

        docente = Personal(nombre=nombre, apellido=apellido, dni=dni, mail=mail,es_docente=es_docente, es_nodo=es_nodo, es_fcejs=es_fcejs)
        docente.save()
    number = docentes_fica.count()
    ctx = {
        'number' : number }
    return render(request, 'personal/success.html', ctx)

"""
