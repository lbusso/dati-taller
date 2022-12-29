from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django.forms import ModelForm
from .models import *
from django import forms
from django.forms.widgets import CheckboxSelectMultiple

#Formulario de inventario y prestamos

class PrestamoForm(ModelForm):
    class Meta:
        model = Prestamo
        exclude = [
            'devuelto',
        ]

class DevolverPrestamoForm(ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'devuelto',
        ]
#FOrmularios CLientes
class AulaCreateForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = '__all__'
        widgets = {
            'equipamiento': forms.CheckboxSelectMultiple()
        }

class AulaEditForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = '__all__'
        widgets = {
            'equipamiento': forms.CheckboxSelectMultiple()
        }


class ClienteCreateForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = '__all__'


#Forms sistema taller
class EquipoCreateForm(ModelForm):
    class Meta:
        model = Equipo
        exclude = ['en_reparacion', 'en_taller']


class EquipoEditForm(ModelForm):
    class Meta:
        model = Equipo
        exclude = ['en_reparacion', 'en_taller']


class EnviarARepararForm(ModelForm):
    class Meta:
        model = Equipo
        fields = ['en_reparacion', 'lugar_reparacion']


class OrdenAulaCreateForm(ModelForm):
    class Meta:
        model = OrdenDeServicioEnAula
        fields = ['aula', 'tecnico', 'motivo']
        exclude = ['ticket', 'estado',]

    def __init__(self, *args, **kwargs):
        super(OrdenAulaCreateForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')

class OrdenDomicilioCreateForm(ModelForm):
    class Meta:
        model = OrdenDeServicioADomicilio
        fields = ['cliente', 'tecnico', 'motivo_servicio', 'observaciones']
        exclude = ['ticket', 'estado','solucion_implementada']

    def __init__(self, *args, **kwargs):
        super(OrdenDomicilioCreateForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')


class OrdenTallerCreateForm(ModelForm):
    class Meta:
        model = OrdenDeServicioEnTaller
        fields = '__all__'
        exclude = ['ticket', 'solucion_implementada', 'estado', 'entregado']

    def __init__(self, *args, **kwargs):
        super(OrdenTallerCreateForm, self).__init__(*args, **kwargs)
        self.fields['equipo'].queryset = Equipo.objects.filter(en_taller=False)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')


class InformeTallerForm(ModelForm):
    class Meta:
        model = InformeTaller
        fields = ['informe']


class TransferirOrdenForm(ModelForm):
    class Meta:
        model = OrdenDeServicioEnTaller
        fields = ['tecnico']

    def __init__(self, *args, **kwargs):
        super(TransferirOrdenForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')


class TerminarOrdenForm(ModelForm):
    class Meta:
        model = OrdenDeServicioEnTaller
        fields = ['estado', 'solucion_implementada']

class EntregarOrdenForm(ModelForm):
    class Meta:
        model = OrdenDeServicioEnTaller
        fields = ['entregado']


class InformeDomicilioForm(ModelForm):
    class Meta:
        model = InformeDomicilio
        fields = ['informe']


class TerminarDomicilioForm(ModelForm):
    class Meta:
        model = OrdenDeServicioADomicilio
        fields = ['estado', 'solucion_implementada']


class TransferirdomicilioForm(ModelForm):
    class Meta:
        model = OrdenDeServicioADomicilio
        fields = ['tecnico']

    def __init__(self, *args, **kwargs):
        super(TransferirdomicilioForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')


class InformeAulaForm(ModelForm):
    class Meta:
        model = InformeAula
        fields = ['informe']


class TransOrdeAulaForm(ModelForm):
    class Meta:
        model = OrdenDeServicioEnAula
        fields = ['tecnico']
    def __init__(self, *args, **kwargs):
        super(TransOrdeAulaForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')


class TerminarOrdenAulaForm(ModelForm):
    class Meta:
        model = OrdenDeServicioEnAula
        fields = ['estado', 'solucion_implementada']

# Eventos

class DateInput(forms.DateInput):
    input_type = 'date'
    imput_format = '%d-%m-%y'
class TimeInput(forms.TimeInput):
    input_type = 'time'
    input_format = '%HH:%MM'

class EventoCreateForm(ModelForm):

    class Meta:
        model = Evento
        fields = ['titulo', 'cliente', 'aula', 'tecnico', 'fecha', 'hora', 'hora_fin', 'lista_elementos']
        widgets = {
            'fecha': DateInput(),
            'hora':TimeInput(format='%HH:%MM'),
            'hora_fin': TimeInput(format='%HH:%MM'),
            'lista_elementos': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(EventoCreateForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')

class EventoEditForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'cliente', 'aula', 'tecnico', 'fecha', 'hora','hora_fin', 'lista_elementos']
        widgets = {
            'fecha': DateInput(),
            'hora': TimeInput(),
            'hora_fin': TimeInput(format='%HH:%MM'),
            'lista_elementos': forms.CheckboxSelectMultiple()
        }

class TerminarEventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['terminado']


class TransfEventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['tecnico']

    def __init__(self, *args, **kwargs):
        super(TransfEventoForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = User.objects.filter(groups__name='Tecnicos')
