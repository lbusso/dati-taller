from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources



class PersonalFICAResourse(resources.ModelResource):
    class Meta:
        model = Personal

class PersonalFICAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['apellido', 'nombre',  'dni', 'mail' ,'is_active']
    search_fields = ['nombre', 'apellido', 'dni']
    ordering = ['apellido']




admin.site.register(Personal, PersonalFICAdmin)
