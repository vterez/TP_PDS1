from .models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse
from hashlib import blake2s as khash
from django.db import IntegrityError
from django.utils.timezone import now
import csv
from datetime import datetime

def msort(e):
    return e[0]

def OrganizaHorarios():
    horarios = HorarioLivre.objects.values_list("id","horario")
    horarios_formatados = []
    for i in range(len(horarios)):
        horarios_formatados.append((horarios[i][0],horarios[i][1].strftime("Dia %d/%m as %H:%M")))
    return horarios_formatados

def decode_utf8(input_iterator):
    """Função decodificadora para abertura dos arquivos csv"""
    for l in input_iterator:
        yield l.decode('utf-8')
        
def Inicial(request):
    horarios = sorted(OrganizaHorarios(),key=msort)
    if horarios:
        return render(request,'myform.html',{"failed":"","horarios":horarios})
    else:
        return render(request,'failed.html',{'failed':'Não há horários disponíveis. Favor contatar o Pedro.'})

def Confirm(request):
    post = request.POST
    if 'opcao' not in post:
        horarios = sorted(OrganizaHorarios(),key=msort)
        return render(request,'myform.html',{"failed":"Horário indisponível. Alguém selecionou esse horário enquanto você decidia. Por favor, selecione outro","horarios":horarios})
    opcao = post["opcao"]
    matricula = post['matricula']
    try:
        mat = Matricula.objects.get(matricula=matricula)
    except:
        horarios = sorted(OrganizaHorarios(),key=msort)
        return render(request,'myform.html',{'failed':f"Número de matrícula não cadastrado na turma. O número informado foi {matricula}","horarios":horarios
        })
    try:
        livre = HorarioLivre.objects.get(id=opcao)
        marcar = livre.horario
        num = livre.id
        marcado = HorarioMarcado(opcao,marcar,post["matricula"],post['nome'],post["email"],num)
        marcado.save()
        livre.delete()
    except HorarioLivre.DoesNotExist:
        horarios = sorted(OrganizaHorarios(),key=msort)
        if horarios:
            return render(request,'myform.html',{"failed":"Horário indisponível. Alguém selecionou esse horário enquanto você decidia. Por favor, selecione outro","horarios":horarios})
        else:
            return render(request,'failed.html',{'failed':'Não há horários disponíveis. Favor contatar o Pedro.'})
    except IntegrityError:
        antigo = HorarioMarcado.objects.get(matricula=matricula)
        dt = antigo.horario
        id = antigo.num
        antigo.delete()
        livre.delete()
        livre = HorarioLivre(dt,id)
        marcado.save()
        livre.save()
        mystr = f'{post["matricula"]}_{post["opcao"]}'.encode('utf8')
        val = str(khash(mystr).hexdigest())
        hora = f'{marcado.horario.hour:02d}:{marcado.horario.minute:02d}'
        dia = f'{marcado.horario.day:02d}/{marcado.horario.month:02d}'
        return render(request,'code.html',{"obs":"Já foi selecionado um horário para seu número de matrícula, então, ele foi liberado e o novo horário foi alocado","code":val,'hora':hora,'dia':dia,'nome':post['nome'],'matricula':matricula})
    except Exception as ex:
        return render(request,'failed.html',{"failed":"Erro inesperado, por favor, mande um email para o monitor Vitor com um print dessa tela","ex":ex})
    mystr = f'{post["matricula"]}_{post["opcao"]}'.encode('utf8')
    val = str(khash(mystr).hexdigest())
    hora = f'{marcado.horario.hour:02d}:{marcado.horario.minute:02d}'
    dia = f'{marcado.horario.day:02d}/{marcado.horario.month:02d}'
    return render(request,'code.html',{"code":val,'hora':hora,'dia':dia,'nome':post['nome'],'matricula':matricula})

def Upload(request):
    return render(request,'upload.html',{'data':'','erro':''})

def Uploaded(request):
    reader = csv.reader(decode_utf8(request.FILES['csvfile']))
    if request.POST['opcao'] == 'Matrículas':
        erro = []
        j=0
        for i in reader:
            try:
                matricula = Matricula(matricula=int(i[0]))
                matricula.save()
                j+=1
            except BaseException as ex:
                print(ex)
                erro.append(i[0])

    else:
        year = now().year
        j=0
        erro = []
        for n,i in enumerate(reader,len(HorarioLivre.objects.all())):
            try:
                if len(i) == 2:
                    day,month = map(int,i[0].split('/'))
                    hour,minute = map(int,i[1].split(':'))
                    dt = datetime(hour=hour,minute=minute,month=month,day=day,year=year,second=0)
                    livre = HorarioLivre(horario=dt,id=n)
                    livre.save()
                    j+=1
                else:
                    erro.append(str(n+1))
            except:
                erro.append(str(n+1))
        
    return render(request,'upload.html',{'data':f'{j} entradas foram adicionadas','erro':';'.join(erro)})
    
