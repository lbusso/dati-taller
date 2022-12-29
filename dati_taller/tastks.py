from celery import shared_task
from django.core.mail import  EmailMultiAlternatives

@shared_task()
def send_email_taller(subject, titulo, mensaje, email):
    msg = EmailMultiAlternatives(subject, titulo, 'Taller <dati@fica.unsl.edu.ar>', [email], bcc=[''])
    msg.attach_alternative(mensaje, "text/html")
    msg.send()
    return None

