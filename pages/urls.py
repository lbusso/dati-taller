from django.urls import path
from .views import *
urlpatterns = [
    path('sistemas/', Home.as_view(), name='home'),
    path('accesodenegado/', AccesoDenegado.as_view(), name='acceso_denegado'),
    path('', redirectview, name='redirect'),
]