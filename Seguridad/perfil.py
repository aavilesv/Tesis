from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Tesis.funciones import addUserData

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

@login_required(login_url='/seguridad/login/')
def perfil(request):
    data ={
        'titulo':'Perfil-FULL AUTO MILAGRO',
        'model': 'Usuario',
        'ruta':'/seguridad/perfil/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():

                    if action == 'edit':
                        us=User.objects.get(pk=int(request.user.id))
                        if (request.POST['chancontr']) == '1':
                            us.set_password(request.POST['password'])
                        print(request.POST['username'])
                        us.username, us.email,us.first_name = request.POST['username'],request.POST['email'],request.POST['first_name']
                        us.last_name ,us.username= request.POST['last_name'], request.POST['username']
                        us.save()

            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/seguridad/perfil/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            data['action'] = request.GET['action']
            if not (request.GET['action'] == 'add'):
                data['id'] = request.GET['id']
                print(request.user.id)
                print(User.objects.get(id=request.user.id))
                data['empleado'] = User.objects.get(id=request.user.id)
            return render(request, 'seguridad/perfil_form.html', data)
        else:
            # Viaja por get

            data['empleado'] = User.objects.get(id=request.user.id)
            return render(request, 'seguridad/perfil.html', data)
