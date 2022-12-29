from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginRequiredMixin,TemplateView):
    template_name = 'pages/home.html'


class AccesoDenegado(TemplateView):
    template_name = 'pages/acceso_denegado.html'

def redirectview(request):
    return redirect('orden_list')