from datetime import datetime
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.generic import CreateView, UpdateView, ListView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
import sweetify
from sweetify.views import SweetifySuccessMixin
from .models import *
from personal.models import Personal
from .forms import *
from .tastks import send_email_taller
import datetime


# Sistema de prestamos e inventario


class ProductoParaPrestarCreate(LoginRequiredMixin, PermissionRequiredMixin, SweetifySuccessMixin, CreateView):

    permission_required = ['dati_taller.is_tecnico']
    model = ProductoParaPrestar
    template_name = 'dati_taller/inventario/producto_prestamo_create.html'
    success_url = reverse_lazy('prd_prestar_list')
    fields = '__all__'
    sweetify_options = {
        'icon': 'success'
    }
    success_message = 'Nuevo Producto Generado'


class ProductoParaPrestarList(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = ['dati_taller.is_tecnico']
    model = ProductoParaPrestar
    template_name = 'dati_taller/inventario/producto_prestamos_list.html'


@login_required(login_url='account_login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def prestamo_list(request):

    prestamos = Prestamo.objects.filter(devuelto=False,)

    context = {
        'prestamo': prestamos
    }
    return render(request, 'dati_taller/inventario/prestamo_list.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def prestamoCreate(request):

    form = PrestamoForm()
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            producto = form.instance.producto
            if producto.cantidad <=0:
                sweetify.error(request,
                               title='ERROR!',
                               text='No se puede realizar el prestamo porque ' + producto.nombre + ' no esta en Stock',
                               icon='error',
                               persistent='Entiendo',
                )
            else:
                producto.cantidad -=1
                producto.save()
                form.save()
                sweetify.success(request, icon='success', title='Prestamo realizado')
                sweetify.success(request,
                                  icon='info',
                                  title='Atención',
                                  text='Ahora nos quedan '+str(producto.cantidad) +' ' + producto.nombre+'para prestar.')
        return redirect('prestamo_list')

    context = {
        'form': form
    }
    return render(request, 'dati_taller/inventario/prestamo_create.html', context)
@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def prestamo_devolver(request, pk):

    prestamo = Prestamo.objects.get(id=pk)
    form = DevolverPrestamoForm(instance=prestamo)

    if request.method == 'POST':
        form = DevolverPrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.instance.devuelto = True
            producto = form.instance.producto
            producto.cantidad += 1
            producto.save()
            form.save()
            sweetify.success(request,title='Excelente',
                             text='Ahora tenemos '+ str(producto.cantidad)+ ' '+producto.nombre + ' en stock')
        else:
            sweetify.error(request, 'Algo salio mal')
        return redirect('prestamo_list')

    context = {
        'form': form,
        'prestamo': prestamo,
    }
    return render(request, 'dati_taller/inventario/prestamo_devolver.html', context)


#VIsta de clientes
class CreateClient(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = ['dati_taller.is_tecnico']
    model = Personal
    fields = '__all__'
    template_name = 'dati_taller/clientes/cliente_create.html'
    success_url = reverse_lazy('cliente_list')

class CrearCLienteModal(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = ['dati_taller.is_tecnico']
    def get(self, request):
        form = ClienteCreateForm()

        context = {
            'form': form,
        }
        return render(request, 'dati_taller/clientes/cliente_create_modal.html', context)

    def post(self, request):

        form = ClienteCreateForm(request.POST)

        if form.is_valid():
            new_client = form.save()
            return JsonResponse({'client': model_to_dict(new_client)}, status=200)

        else:
            return redirect('dati_taller/cliente_list')

@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def clienteCreate(request):

    form = ClienteCreateForm()

    if request.method == 'POST':
        form = ClienteCreateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('dati_taller/cliente_list')
    else:
        messages.error(request, 'Error en los datos ingresados')
    context = {'form': form}

    return render(request, 'dati_taller/clientes/cliente_create_modal.html', context)

class ClienteList(LoginRequiredMixin, PermissionRequiredMixin,ListView):

    permission_required = ['dati_taller.is_tecnico']
    model = Personal
    template_name = 'dati_taller/clientes/cliente_list.html'


class ClienteEdit(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):

    permission_required = ['dati_taller.is_tecnico']
    model = Personal
    template_name = 'dati_taller/clientes/cliente_update.html'
    success_url = reverse_lazy('cliente_list')
    fields = '__all__'


class AulaCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = ['dati_taller.is_tecnico']
    model = Aula
    template_name = 'dati_taller/clientes/aula_create.html'
    form_class = AulaCreateForm
    success_url = reverse_lazy('aula_list')

class AulaList(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = ['dati_taller.is_tecnico']
    model = Aula
    template_name = 'dati_taller/clientes/aula_list.html'


class AulaEdit(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):

    permission_required = ['dati_taller.is_tecnico']
    model = Aula
    template_name = 'dati_taller/clientes/aula_edit.html'
    success_url = reverse_lazy('aula_list')
    form_class = AulaEditForm

class CrearAulaModal(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = ['dati_taller.is_tecnico']
    def get(self, request):
        form = AulaCreateForm()

        context = {
            'form': form,
        }
        return render(request, 'dati_taller/clientes/aula_create_modal.html', context)

    def post(self, request):
        form = AulaCreateForm(request.POST)
        if form.is_valid():
            new_aula = form.save()
            return JsonResponse({'client': model_to_dict(new_aula)}, status=200)

        else:
            return redirect('aula_list')


#Vistas de cuestiones de taller
class EquipoCreate(LoginRequiredMixin, PermissionRequiredMixin, SweetifySuccessMixin, CreateView):

    permission_required = ['dati_taller.is_tecnico']
    model = Equipo
    template_name = 'dati_taller/taller/equipos/equipo_create.html'
    form_class = EquipoCreateForm
    success_url = reverse_lazy('equipo_list')
    sweetify_options = {
        'showConfirmButton': False,
        'timer': 2500,
        'allowOutsideClick': True,
        'confirmButtonText': 'OK',
        'icon': 'success'
    }
    success_message = 'Equipo Creado correctamente'
@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def equipoCreate(request):

    form = EquipoCreateForm()
    if request.method == 'POST':
        form = EquipoCreateForm(request.POST)
        equipo = Equipo.objects.get(codigo=form.instance.cdigo)
        if not equipo:
            if form.is_valid():
                form.save()
                sweetify.success(request,
                                 title='Exclente!',
                                 text='El equipo fue creado con exito',
                                 icon='success',
                                     )
                return redirect('equipo_list')
        else:
            sweetify.error(request,
                           title='Hubo un error!',
                           text='Probablemente el equipo ya existe, verfique elcodigo y vuelva a intentarlo',
                           icon='error',
                           )
            return redirect('equipo_list')



class CrearEquipoModal(LoginRequiredMixin, PermissionRequiredMixin,SweetifySuccessMixin, View):

    permission_required = ['dati_taller.is_tecnico']
    def get(self, request):
        form = EquipoCreateForm()

        context = {
            'form': form,
        }
        return render(request, 'dati_taller/taller/equipos/equipo_create_modal.html', context)

    def post(self, request):
        form = EquipoCreateForm(request.POST)

        if form.is_valid():
            new_equipo = form.save()
            sweetify.success(request, 'Equipo credo Correctamente', icon='success')
            return JsonResponse({'equipo': model_to_dict(new_equipo)}, status=200)

        else:
         return redirect('equipo_list')


class EquipoEdit(LoginRequiredMixin, PermissionRequiredMixin, SweetifySuccessMixin, UpdateView):

    permission_required = ['dati_taller.is_tecnico']
    model = Equipo
    template_name = 'dati_taller/taller/equipos/equipo_update.html'
    form_class = EquipoEditForm
    success_url = reverse_lazy('equipo_list')
    sweetify_options = {
        'showConfirmButton': False,
        'timer': 2500,
        'allowOutsideClick': True,
        'confirmButtonText': 'OK',
        'icon': 'success'
    }
    success_message = 'Equipo Editado correctamente'


class EquipoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = ['dati_taller.is_tecnico']
    model = Equipo
    template_name = 'dati_taller/taller/equipos/equipo_list.html'


# Ordenes de servicio en taller

@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenesEntaller(request):

    if request.user.is_superuser:
        ordenes_en_taller = OrdenDeServicioEnTaller.objects.filter(entregado=False, )
    else:
        ordenes_en_taller = OrdenDeServicioEnTaller.objects.filter(entregado=False, tecnico=request.user)

    context = {'ordenes': ordenes_en_taller}

    return render(request, 'dati_taller/taller/servicio-en-taller/ordenes_list.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenTallerDetail(request, pk):

    orden = OrdenDeServicioEnTaller.objects.get(id=pk)
    informes = orden.informetaller_set.all()

    context = {'orden': orden, 'informes': informes}
    return render(request, 'dati_taller/taller/servicio-en-taller/orden-detalle.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenTallerCreate(request):

    form = OrdenTallerCreateForm()
    if request.method == 'POST':
        form = OrdenTallerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            equipo = Equipo.objects.get(codigo=form.instance.equipo.codigo)
            equipo.en_taller = True
            equipo.save()

            #Envia Email al tecnico responsable de la orden
            motivo = form.instance.motivo_ingreso.motivo
            observaciones = form.instance.observaciones
            tecnico = form.instance.tecnico
            subject = "Nueva orden en taller a tu nombre"
            email = tecnico.email
            tiket = form.instance.ticket
            ctx= {
                        'nombre': tecnico,
                        'ticket': tiket,
                        'motivo': motivo,
                        'observaciones': observaciones,
                    }
            mensaje = loader.render_to_string('dati_taller/email/new_orden_mail.html', ctx)
            send_email_taller.delay(subject, motivo, mensaje, email)

            sweetify.success(request,
                             title='Exclente!',
                             text='La orden fue creada satisfactoriamente',
                             icon='success',
                             )

        return redirect('orden_list')

    context = {'form': form, 'messages': messages}

    return render(request, 'dati_taller/taller/servicio-en-taller/orden-taller-new.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def informeTaller(request, pk):

    orden = OrdenDeServicioEnTaller.objects.get(id=pk)
    form = InformeTallerForm(initial={'orden': orden})

    if request.method == 'POST':
        form = InformeTallerForm(request.POST)
        if form.is_valid():
            orden.estado = 'En Proceso'
            orden.save()
            form.instance.orden = orden
            form.instance.tecnico = request.user
            form.save()
            sweetify.success(request, 'Informe Agregado satisfactoriamente')
        else:
            sweetify.error(request, 'A ocurrido un error')

        return redirect('orden_detail', pk)

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-taller/informe.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def transferirOrden(request, pk):

    orden = OrdenDeServicioEnTaller.objects.get(id=pk)
    form = TransferirOrdenForm(instance=orden)

    if request.method == 'POST':
        form = TransferirOrdenForm(request.POST or None, instance=orden)
        if form.is_valid():
            form.save()
            sweetify.success(request, title='Correcto!', text='Transerido a '+ form.instance.tecnico.get_full_name(),)
        else:
            sweetify.error(request, title='Ocurrio un problema', icon='error')
        return redirect('orden_detail', pk)

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-taller/transferir.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def enviarAReparar(request, pk):
    equipo = Equipo.objects.get(id=pk)
    form = EnviarARepararForm()
    if request.method == "POST":
        form = EnviarARepararForm(request.POST, instance=equipo)
        if form.is_valid():
            form.instance.en_reparacion = True
            form.save()
            sweetify.success(request, title='Enviado a reparacion!')
        else:
            sweetify.error(request, title='Ocurrio un problema', icon='error')
        return redirect('orden_list')

    context = {'form': form, 'orden': equipo}

    return render(request, 'dati_taller/taller/servicio-en-taller/enviar_reparar.html', context)

@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def volverDeReparar(request, pk):

    equipo = Equipo.objects.get(id=pk)
    form = EnviarARepararForm()

    if request.method == "POST":
        form = EnviarARepararForm(request.POST, instance=equipo)
        if form.is_valid():
            form.instance.en_reparacion = False
            form.save()
            sweetify.success(request, title='Devuelto de reparacion!')
        else:
            sweetify.error(request, title='Ocurrio un problema', icon='error')
        return redirect('orden_list')

    context = {'form': form, 'orden': equipo}

    return render(request, 'dati_taller/taller/servicio-en-taller/volver_de_reparar.html', context)

@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def terminarOrden(request, pk):

    orden = OrdenDeServicioEnTaller.objects.get(id=pk)
    motivo = orden.motivo_ingreso
    form = TerminarOrdenForm(request.POST or None, initial={'motivo_ingreso': motivo})
    form.fields['solucion_implementada'].queryset = SolucionAMotivoOrdenEnTaller.objects.filter(motivo=motivo)
    equipo = orden.equipo


    if request.method == "POST":
        form = TerminarOrdenForm(request.POST, instance=orden,)

        if form.is_valid():
            equipo.en_reparacion = False
            equipo.save()
            form.instance.estado = "Terminado"
            form.instance.en_reparacion = False
            form.save()

            sweetify.success(request, title='Orden Terminada', text='Orden lista para entregar!')
        else:
            sweetify.success(request, title='Ocurrio un error')

        return redirect('orden_detail', pk)

    context = {'form': form, 'orden': orden , }

    return render(request, 'dati_taller/taller/servicio-en-taller/orden_terminar.html', context)


class OrdenResult(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    permission_required = ['dati_taller.is_tecnico']
    model = OrdenDeServicioEnTaller
    template_name = 'dati_taller/taller/equipos/equipo_result.html'
    context_object_name = 'orden'
    def get_queryset(self):
        query = self.request.GET.get("s")
        return OrdenDeServicioEnTaller.objects.filter(
             Q(equipo__codigo__exact=query)
        )


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def EntregarOrden(request, pk):

    orden = OrdenDeServicioEnTaller.objects.get(id=pk)
    equipo = orden.equipo
    form = EntregarOrdenForm()

    if request.method == "POST":
        form = EntregarOrdenForm(request.POST, instance=orden)
        if form.instance.estado == "Terminado":
            if form.is_valid():
                form.instance.entregado = True
                form.instance.estado = "Terminado"
                form.save()
                equipo.en_taller = False
                equipo.save()
                sweetify.success(request, title='La orden fue entregada al cliente')
        else:
            sweetify.error(request, title='Debes terminar la orden antes de entrgarla')

        return redirect('orden_list')

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-taller/orden_entregar.html', context)

class RealizarInforme(TemplateView):
    template_name = 'dati_taller/taller/servicio-en-taller/realizar_informe.html'

# Ordenes de servicio a domicilio


class DomicilioCreate(LoginRequiredMixin, PermissionRequiredMixin, SweetifySuccessMixin, CreateView):

    permission_required = ['dati_taller.is_tecnico']
    model = OrdenDeServicioADomicilio
    form_class = OrdenDomicilioCreateForm
    template_name = 'dati_taller/taller/servicio-en-domicilio/orden-domicilio-create.html'
    success_url = reverse_lazy('domicilio_list')

    sweetify_options = {
        'icon': 'success'
    }
    success_message = 'Equipo Creado correctamente'

    #Enviar email al tecnico responsable
    def form_valid(self, form):
        form.instance.imagen = self.request.FILES.getlist('imagen')
        form.save()
        motivo = form.instance.motivo_servicio.motivo
        observaciones = form.instance.observaciones
        tecnico = form.instance.tecnico
        subject = "Nueva orden de domicilio a tu nombre"
        email = tecnico.email
        tiket = form.instance.ticket

        ctx = {
            'nombre': tecnico,
            'ticket': tiket,
            'motivo': motivo,
            'observaciones': observaciones,
        }
        mensaje = loader.render_to_string('dati_taller/email/new_orden_mail.html', ctx)

        send_email_taller.delay(subject, motivo, mensaje, email)

        return super().form_valid(form)

@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def domicilioList(request):

    if request.user.is_superuser:
        orden = OrdenDeServicioADomicilio.objects.filter().exclude(estado='Terminado')
    else:
        orden = OrdenDeServicioADomicilio.objects.filter(tecnico=request.user).exclude(estado='Terminado')

    context = {'servicio': orden, }

    return render(request, 'dati_taller/taller/servicio-en-domicilio/ordenes-domicilio-list.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenDomicilioDetail(request, pk):

    orden = OrdenDeServicioADomicilio.objects.get(id=pk)
    informes = orden.informedomicilio_set.all()

    context = {'orden': orden, 'informes': informes}
    return render(request, 'dati_taller/taller/servicio-en-domicilio/orden-domicilio-detalle.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def informeDomicilio(request, pk):

    orden = OrdenDeServicioADomicilio.objects.get(id=pk)
    form = InformeDomicilioForm(initial={'orden': orden})

    if request.method == 'POST':
        form = InformeDomicilioForm(request.POST)
        if form.is_valid():
            orden.estado = 'En Proceso'
            orden.save()
            form.instance.orden = orden
            form.instance.tecnico = request.user
            form.save()
            sweetify.success(request, title='Informe generado correctamente')
        return redirect('domicilio_detail', pk)

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-domicilio/informe.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def terminarOrdenDomicilio(request, pk):

    orden = OrdenDeServicioADomicilio.objects.get(id=pk)
    motivo = orden.motivo_servicio
    form = TerminarDomicilioForm(request.POST or None, initial={'motivo_servicio': motivo})
    form.fields['solucion_implementada'].queryset = SolucionAMotivoOrdenEnDomicilio.objects.filter(motivo=motivo)


    if request.method == "POST":
        form = TerminarDomicilioForm(request.POST, instance=orden)
        if form.is_valid():
            form.instance.estado = "Terminado"
            form.save()
            sweetify.success(request, 'Orden terminada satisfactoriamente')

        return redirect('domicilio_list')

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-domicilio/orden-domicilio-terminar.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def transferirDomicilio(request, pk):

    orden = OrdenDeServicioADomicilio.objects.get(id=pk)
    form = TransferirdomicilioForm(instance=orden)

    if request.method == 'POST':
        form = TransferirOrdenForm(request.POST or None, instance=orden)
        if form.is_valid():
            form.save()
            sweetify.success(request, title='Correcto!', text='La orden fue transferida a '+ form.instance.tecnico.get_full_name())
        else:
            sweetify.error(request, title='Algo salio mal :(')

        return redirect('domicilio_detail', pk)

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-domicilio/transferir.html', context)


# Ordenes de Servicio en Aulas

class OrdenAulaCreate(LoginRequiredMixin, PermissionRequiredMixin, SweetifySuccessMixin, CreateView):
    permission_required = ['dati_taller.is_tecnico']
    model = OrdenDeServicioEnAula
    template_name = 'dati_taller/taller/servicio-en-aula/orden-aula-create.html'
    form_class = OrdenAulaCreateForm
    success_url = reverse_lazy('servicio_aula_list')
    sweetify_options = {
        'icon': 'success'
    }
    success_message = 'Orden creada Satisfactoriamente'


    #Enviar email al tecnico responsable
    def form_valid(self, form):
        motivo = form.instance.motivo.motivo
        aula = form.instance.aula
        tecnico = form.instance.tecnico
        subject = "Nueva orden en aula a tu nombre"
        email = tecnico.email
        tiket = form.instance.ticket

        ctx = {
            'nombre': tecnico,
            'ticket': tiket,
            'motivo': motivo,
            'observaciones': aula,
        }
        mensaje = loader.render_to_string('dati_taller/email/new_orden_mail.html', ctx)
        send_email_taller.delay(subject, motivo, mensaje, email)

        return super().form_valid(form)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenAulaList(request):
    if request.user.is_superuser:
        orden = OrdenDeServicioEnAula.objects.filter().exclude(estado='Terminado')
    else:
        orden = OrdenDeServicioEnAula.objects.filter(tecnico=request.user).exclude(estado='Terminado')

    context = {'servicio': orden, }

    return render(request, 'dati_taller/taller/servicio-en-aula/ordenes-aula-list.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenAulaDetail(request, pk):
    orden = OrdenDeServicioEnAula.objects.get(id=pk)
    informes = orden.informeaula_set.all()

    context = {'orden': orden, 'informes': informes}
    return render(request, 'dati_taller/taller/servicio-en-aula/orden-aula-detalle.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def informeAula(request, pk):
    orden = OrdenDeServicioEnAula.objects.get(id=pk)
    form = InformeAulaForm(initial={'orden': orden})

    if request.method == 'POST':
        form = InformeAulaForm(request.POST)
        if form.is_valid():
            orden.estado = 'En Proceso'
            orden.save()
            form.instance.orden = orden
            form.instance.tecnico = request.user
            form.save()
            sweetify.success(request, title='Informe generado Correctamente')
        else:
            sweetify.error(request, title='Algo salio mal!')
        return redirect('servicio_aula_detail', pk)

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-aula/informe.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def transferirOrdenAula(request, pk):
    orden = OrdenDeServicioEnAula.objects.get(id=pk)
    form = TransOrdeAulaForm(instance=orden)

    if request.method == 'POST':
        form = TransOrdeAulaForm(request.POST or None, instance=orden)
        if form.is_valid():
            form.save()
            sweetify.success(request, title='Correcto!', text='La orden fue transferida a'+ form.instance.tecnico.get_full_name())
        else:
            sweetify.error(request, title='Algo salio mal!')

        return redirect('servicio_aula_detail', pk)

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-aula/transferir.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def terminarOrdenAula(request, pk):
    orden = OrdenDeServicioEnAula.objects.get(id=pk)
    motivo = orden.motivo
    form = TerminarOrdenAulaForm(request.POST or None, initial={'motivo_servicio': motivo})
    form.fields['solucion_implementada'].queryset = SolucionAMotivoOrdenEnAula.objects.filter(motivo=motivo)

    if request.method == "POST":
        form = TerminarOrdenAulaForm(request.POST, instance=orden)
        if form.is_valid():
            form.instance.estado = "Terminado"
            form.save()
            sweetify.success(request, title='El problema fue resuelto!', icon='success')

        return redirect('servicio_aula_list')

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/servicio-en-aula/orden-aula-terminar.html', context)


# Ordenes de Eventos
@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def evento_create(request):
    form = EventoCreateForm()

    if request.method == 'POST':
        form = EventoCreateForm(request.POST)

        """Datos de formulario"""
        fecha = form['fecha'].value()
        hora_inicio = datetime.datetime.strptime(form['hora'].value(),"%H:%M").time()
        lista_elementos= form['lista_elementos'].value()
        lista_elementos = [int(i) for i in lista_elementos]

        evento = Evento.objects.all().filter(fecha=fecha, terminado=False).last()

        if evento:
            """Datos de evento para comprar"""
            date = datetime.date(1, 1, 1)
            time = datetime.timedelta(hours=3)
            elementos = [elemento for elemento in evento.lista_elementos.all().values_list('id',  flat=True)]
            evento1 = datetime.datetime.combine(date, evento.hora_fin)
            evento2 = datetime.datetime.combine(date, hora_inicio)
            diferencia = abs((evento2 - evento1))

            #Si hay tiempo suficiente...
            if diferencia >= time:
                comparacion = []
                recuperacion = []


                for item in lista_elementos:
                    if item in elementos:
                        comparacion.append(item)

                for id in comparacion:
                    elemento = ElementosParaEventos.objects.get(id=id)
                    recuperacion.append(elemento.nombre)

                if len(comparacion)> 0:
                    if form.is_valid():
                        evento = form.save(commit=False)
                        evento.tecnico = form.instance.tecnico
                        evento.save()
                        form.save_m2m()

                    subject = "Nuevo evento a tu nombre"
                    tecnico = form.instance.tecnico
                    responsable = tecnico.get_full_name()
                    email = tecnico.email
                    titulo = form.instance.titulo
                    ctx = {
                        'responsable': responsable,
                        'titulo': titulo,

                    }
                    mensaje = loader.render_to_string('dati_taller/email/dati-evento.html', ctx)

                    send_email_taller.delay(subject, titulo, mensaje, email)

                    sweetify.info(request, title='El evento se creó pero hay elementos prestados el mismo dia, asegurse de recuperarlos antes.',
                                  text=('Recuperar: %s' % (recuperacion)),
                                  button='Ok',
                                  timer=20000,
                                  timerProgressBar='true',
                                  )

                else:
                    if form.is_valid():
                        evento = form.save(commit=False)
                        evento.tecnico = form.instance.tecnico
                        evento.save()
                        form.save_m2m()

                    subject = "Nuevo evento a tu nombre"
                    tecnico = form.instance.tecnico
                    responsable = tecnico.get_full_name()
                    email = tecnico.email
                    titulo = form.instance.titulo
                    ctx = {
                        'responsable': responsable,
                        'titulo': titulo,

                    }
                    mensaje = loader.render_to_string('dati_taller/email/dati-evento.html', ctx)

                    send_email_taller.delay(subject, titulo, mensaje, email)

                    sweetify.info(request, title='Hay tiempo suficiente, no hay elementos necesarios Prestados, el evento se crea normalmente.',
                                  button='Ok',
                                  timer=20000,
                                  timerProgressBar='true',
                                  )

            else:
                sweetify.warning(request,
                                 title='No existe tiempo suficiente para preparar este evento, porque ya existe uno en el mismo dia. Asegurese de que exista al menos 3 hs de diferencia entre eventos.',
                                 button='Entiendo',
                                 timer= 10000,
                                 timerProgressBar='true',
                                 )
        else:
            if form.is_valid():
               evento =form.save(commit=False)
               evento.tecnico = form.instance.tecnico
               evento.save()
               form.save_m2m()

            subject = "Nuevo evento a tu nombre"
            tecnico = form.instance.tecnico
            responsable = tecnico.get_full_name()
            email = tecnico.email
            titulo = form.instance.titulo
            ctx = {
                'responsable': responsable,
                'titulo': titulo,

            }
            mensaje = loader.render_to_string('dati_taller/email/dati-evento.html', ctx)

            send_email_taller.delay(subject, titulo, mensaje, email)
            sweetify.toast(request, title='Evento creado Correctamente', icon='success')

        return redirect('evento_list')

    context = {'form': form}
    return render(request, 'dati_taller/taller/eventos/evento-create.html', context)


class EventoEdit(LoginRequiredMixin, PermissionRequiredMixin, SweetifySuccessMixin, UpdateView):
    permission_required = ['dati_taller.is_tecnico']
    model = Evento
    form_class = EventoEditForm
    template_name = 'dati_taller/taller/eventos/evento-edit.html'
    success_url = reverse_lazy('evento_list')
    sweetify_options = {
        'icon': 'success'
    }
    success_message = 'Evento Editado Correctamente'

@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenEventoList(request):
    if request.user.is_superuser:
         orden = Evento.objects.filter().exclude(terminado=True)
    else:
         orden = Evento.objects.filter(tecnico=request.user).exclude(terminado=True)

    context = {'servicio': orden, }

    return render(request, 'dati_taller/taller/eventos/evento-list.html', context)

@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenEventoListHoy(request):
    fecha= datetime.date.today()
    if request.user.is_superuser:
         orden = Evento.objects.filter(fecha=fecha).exclude(terminado=True)
    else:
         orden = Evento.objects.filter(fecha=fecha,tecnico=request.user).exclude(terminado=True)

    context = {'servicio': orden, }

    return render(request, 'dati_taller/taller/eventos/evento-list-hoy.html', context)
@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def ordenEventoDetail(request, pk):
    orden = Evento.objects.get(id=pk)
    informes = orden.informeevento_set.all()

    context = {'orden': orden, 'informes': informes}
    return render(request, 'dati_taller/taller/eventos/evento-detalle.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def terminarEvento(request, pk):
    evento = Evento.objects.get(id=pk)
    form = TerminarEventoForm()

    if request.method == "POST":
        form = TerminarEventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.instance.terminado = True
            form.save()
        return redirect('evento_list')

    context = {'form': form, 'evento': evento}

    return render(request, 'dati_taller/taller/eventos/evento-terminar.html', context)


@login_required(login_url='login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def transferirEvento(request, pk):
    orden = Evento.objects.get(id=pk)
    form = TransfEventoForm(instance=orden)

    if request.method == 'POST':
        form = TransfEventoForm(request.POST or None, instance=orden)
        if form.is_valid():
            form.save()
            sweetify.success(request, title='Transferido', text='Ahora el evento está a cargo de '+ form.instance.tecnico.get_full_name())
        return redirect('evento_detail', pk)

    context = {'form': form, 'orden': orden}

    return render(request, 'dati_taller/taller/eventos/transferir.html', context)


'-------------------------------------------------------------------'
#vistas sistema cdc viejo busqueda por cliente y N de serie
class OldOrdenesList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ['dati_taller.is_tecnico']
    model = Ordenes_old
    template_name = 'dati_taller/sistema_viejo/old_ordenes_list.html'

@login_required(login_url='account_login')
@permission_required('dati_taller.is_tecnico', raise_exception=True)
def old_orden_detail(request, pk):
    orden = Ordenes_old.objects.get(id=pk)
    nserie = int(orden.equipo)
    equipo = Equipo.objects.get(codigo=nserie)
    informes = Informes_old.objects.filter(orden=orden.id)



    context = {'orden': orden, 'equipo': equipo, 'informes': informes}
    return render(request, 'dati_taller/sistema_viejo/old_orden_detail.html', context)

class SearchClientResult(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    permission_required = ['dati_taller.is_tecnico']
    model = Ordenes_old
    template_name = 'dati_taller/sistema_viejo/search_client_result.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Ordenes_old.objects.filter(
             Q(cliente__icontains=query)
        )

class SearchEquipoResult(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    permission_required = ['dati_taller.is_tecnico']
    model = Ordenes_old
    template_name = 'dati_taller/sistema_viejo/search_equipo_result.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Ordenes_old.objects.filter(
             Q(equipo__exact=query)
        )
