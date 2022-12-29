"""dati_project URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('dev-hope/', admin.site.urls),
    path('taller/', include('dati_taller.urls')),
    path('personal/', include('personal.urls')),
    #Urls paginas staticas
    path('', include('pages.urls')),

    #urls autenticacion
    path("accounts/", include("django.contrib.auth.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)