from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from Tesis.funciones import addUserData
from Seguridad.models import *
from django.contrib.auth.models import User, Group
#import geoip2.database
from datetime import timedelta, datetime
import time
#PETICION AJAX
from django.http import JsonResponse,HttpResponse
#Correo2
from django.template.loader import render_to_string
from Tesis.config import *


#reader = geoip2.database.Reader('GeoLite2-City.mmdb')
empresa = NOMBRE_INSTITUCION
ruta= 'https://outlook.live.com/'

@login_required(login_url='/seguridad/login/')
def registro(request):
    data = {
        'model': 'Usuarios',
        'titulo': 'REGISTROS DE USUARIOS',
        'titulo1': 'Listado de Usuarios',
        'titulo2': 'Usuarios',
        'ruta': '/seguridad/usuarios/',
        'user': request.user.username,

    }
    # addUserData(request, data)
    #
    # if request.is_ajax():
    #     if request.GET['action'] == 'elim':
    #         postar = Usuarios.objects.get(id=request.GET['id'])
    #         us = User.objects.get(id=postar.user.id)
    #         if us.is_superuser == False:
    #             User.objects.filter(id=postar.user.id).update(is_active=False)
    #             postar = Usuarios.objects.get(id=request.GET['id'])
    #             nombre= postar.user.username
    #             salva_auditoria(request, postar, 'elim',nombre)
    #         cedula = 'Existe'
    #         response = JsonResponse({'id': cedula})
    #         return HttpResponse(response.content)
    #
    #     else:
    #         c = User.objects.filter(username=request.GET['username']).count()
    #         if c == 1:
    #             username = 'Existe'
    #         else:
    #             username = 'Dale'
    #         response = JsonResponse({'username': username})
    #         return HttpResponse(response.content)
    #
    #
    # if request.method == 'POST':
    #     if 'action' in request.POST:
    #         action = request.POST['action']
    #
    #         try:
    #             with transaction.atomic():
    #
    #                 if action == 'add':
    #                     if request.method == 'POST':
    #                         us = User.objects.create_user(username=request.POST['username'],
    #                                                       first_name=request.POST['first_name'],
    #                                                       last_name=request.POST['last_name'],
    #                                                       email=request.POST['email'],
    #                                                       password=request.POST['password'])
    #                         us.groups.add(request.POST['group'])
    #                         if 'is_staff' in request.POST:
    #                             if request.POST['is_staff'] == 'on':
    #                                 u1 = User.objects.get(username=us)
    #                                 u1.is_staff = True
    #                                 u1.save()
    #                         else:
    #                             u1 = User.objects.get(username=us)
    #                             u1.is_staff = False
    #                             u1.save()
    #                         e= Usuarios(user=us,foto=request.FILES['foto'],telefono=request.POST['telefono'],documento=request.POST['documento'],celular=request.POST['celular'],ubicacion='')
    #                         e.save()
    #                         postar = e
    #                         nombre= postar.user.username
    #                         salva_auditoria(request, postar, action, nombre)
    #                     else:
    #                         messages.error(request,'No se pudo completar esta acción.')
    #                 if action == 'edit':
    #                     if request.method == 'POST':
    #                         consu = Usuarios.objects.get(pk=request.POST['id'])
    #                         u = User.objects.get(pk= consu.user.pk)
    #                         u.first_name = request.POST['first_name']
    #                         u.last_name = request.POST['last_name']
    #                         u.email = request.POST['email']
    #                         u.save()
    #                         g = Group.objects.get(name=str(u.groups.all()[0]))
    #                         u.groups.remove(g.id)
    #                         u.groups.add(request.POST['group'])
    #                         if request.POST['password'] == "":
    #                             pass
    #                         else:
    #                             u.set_password(request.POST['password'])
    #                             u.save()
    #                             messages.success(request, 'Clave restaurada.')
    #                         e = Usuarios.objects.get(id=request.POST['id'])
    #                         e.telefono= request.POST['telefono']
    #                         e.celular= request.POST['celular']
    #                         e.documento= request.POST['documento']
    #                         if 'foto' in request.FILES:
    #                             e.foto = request.FILES['foto']
    #                         e.save()
    #                         postar = Usuarios.objects.get(id=request.POST['id'])
    #                         nombre= postar.user.username
    #                         if 'is_staff' in request.POST:
    #                             if request.POST['is_staff'] == 'on':
    #                                 u.is_staff = True
    #                                 u.save()
    #                         else:
    #                              u.is_staff = False
    #                              u.save()
    #                         if 'activo' in request.POST:
    #                             if request.POST['activo'] == 'on':
    #                                 u.is_active = True
    #                                 u.save()
    #                         else:
    #                              u.is_active = False
    #                              u.save()
    #                         salva_auditoria(request, postar, action, nombre)
    #                     else:
    #                         messages.error(request,'No se pudo completar esta acción')
    #
    #         except Exception as ex:
    #             if '"Cannot delete some instances' in str(ex):
    #                 messages.error(request, 'No se puede eliminar este registro, debido a que esta siendo utilizado por otro!')
    #             elif 'duplicate key value violates unique constraint' in str(ex):
    #                 messages.error(request, 'Usuario ya existe')
    #             else:
    #                 messages.error(request, ex)
    #         return redirect('/seguridad/usuarios/')
    #
    # else:
    #     if 'action' in request.GET:
    #         try:
    #             action = request.GET['action']
    #             grup = Group.objects.all()
    #             data['gro'] = grup
    #             data['action'] = action
    #
    #             if action == 'add':
    #                 pass
    #             if action == 'edit':
    #                 data['accion'] = 'editar'
    #                 id =request.GET['id']
    #                 data['id'] = id
    #                 empleado = Usuarios.objects.get(pk=id)
    #                 data['foto'] = empleado.foto
    #                 data['telefono'] = empleado.telefono
    #                 data['empleado'] = empleado.user
    #                 data['celular'] = empleado.celular
    #                 data['activo'] = empleado.user.is_active
    #                 data['documento'] = empleado.documento
    #                 data['grupo'] = str(empleado.user.groups.all()[0])
    #
    #             if action == 'ver':
    #                 data['accion'] = 'ver'
    #                 id =request.GET['id']
    #                 data['id'] = id
    #                 empleado = Usuarios.objects.get(pk=id)
    #                 data['foto'] = empleado.foto
    #                 data['celular'] = empleado.celular
    #                 data['documento'] = empleado.documento
    #                 data['telefono'] = empleado.telefono
    #                 data['empleado'] = empleado.user
    #                 data['activo'] = empleado.user.is_active
    #                 data['grupo'] = str(empleado.user.groups.all()[0])
    #
    #             if request.user.is_staff == True:
    #                 return render(request,'seguridad/frm_usuarios.html',data)
    #             else:
    #                 return render(request,'page_403.html', data)
    #         except Exception as ex:
    #                 if 'matching query does not exist' in str(ex):
    #                     messages.error(request, 'Registro no existe.')
    #                     return redirect(data['ruta'])
    #                 else:
    #                     messages.error(request, ex)
    #                     return redirect(data['ruta'])
    #
    #     criterio = ""
    #     desde = ""
    #     hasta = ""
    #     if 'criterio' in request.GET:
    #         criterio = request.GET['criterio']
    #         data['criterio'] = criterio
    #     if 'desde' in request.GET:
    #         desde = request.GET['desde']
    #         data['desde'] = desde
    #         data['hasta'] = hasta
    #         if request.GET['hasta']:
    #             hasta = request.GET['hasta']
    #             data['hasta'] = hasta
    #
    #
    #     if criterio and desde == "" and hasta == "":
    #         empleado = Usuarios.objects.filter(Q(user__first_name__icontains=criterio) |
    #                                            Q(user__last_name__icontains=criterio) |
    #                                            Q(user__username__icontains=criterio)).order_by('-id')
    #     else:
    #         # La primera vez viaje por get: consulta todos los datos
    #         empleado = Usuarios.objects.all().order_by('-id')
    #     try:
    #         data['empleado'] = empleado
    #
    #         if request.user.is_staff == True:
    #             return render(request,'seguridad/listar_usuarios.html', data)
    #         else:
    #             return render(request,'page_403.html', data)
    #
    #     except Exception as ex:
    #         if 'That page contains no results' in str(ex):
    #             return render(request,'seguridad/listar_usuarios.html',data)
    #         else:
    #             messages.error(request, ex)
    #             return render(request,'seguridad/listar_usuarios.html',data)