from django.contrib import admin
from .models import *

admin.site.register(HorarioLivre)
admin.site.register(HorarioMarcado,HorarioAdmin)
admin.site.register(Matricula)
# Register your models here.
