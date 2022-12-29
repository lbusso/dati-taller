from django.db import models


class Personal(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    dni = models.BigIntegerField(unique=True)
    mail = models.EmailField(blank=True, null=True)
    box = models.CharField(max_length=150, null=True, blank=True)
    interno = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering= ['apellido']
    def __str__(self):
        return self.apellido + " " + self.nombre

