from django.db import models
from django.utils.translation import ugettext_lazy as lazy
from django.contrib import admin
from django.http import HttpResponse
from django.utils.timezone import now
import csv


def Download_CSV(modeladmin,request,query):
    with open("Dias.csv",mode="w") as arq:
        print(f'Subject,Start date,Start time',file=arq)
        for i in query:
            print(i,file=arq)
    f = open('Dias.csv', 'r')
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Dias.csv'
    return response

class HorarioLivre(models.Model):
    horario = models.DateTimeField(blank=True,null=True,default=now())
    id = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return f'{self.horario.day:02d}/{self.horario.month:02d} -> {self.horario.hour:02d}:{self.horario.minute:02d}'
    
    class Meta:
        verbose_name = lazy("Horário livre")
        verbose_name_plural = lazy("Horários livres")
        
class HorarioMarcado(models.Model):
    horario = models.DateTimeField(null=True,blank=True)
    matricula = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(default="null@null.com")
    num = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.nome},{self.horario.month}/{self.horario.day}/{self.horario.year},{self.horario.hour}:{self.horario.minute}'
    
    class Meta():
        verbose_name = lazy("Horário marcado")
        verbose_name_plural = lazy("Horários marcados")

class HorarioAdmin(admin.ModelAdmin):
    list_display = ('nome','horario')
    actions = [Download_CSV]

class Matricula(models.Model):
    matricula = models.IntegerField(unique=True)
    def __str__(self):
        return str(self.matricula)

    
