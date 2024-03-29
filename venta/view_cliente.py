from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Tesis.funciones import addUserData
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from venta.models import M_CLIENTE


@login_required(login_url='/seguridad/login/')
def cliente(request):
    data ={
        'titulo':'Consulta de Clientes -FULL AUTO MILAGRO',
        'model': 'Cliente',
        'ruta':'/venta/cliente/',
        'user': request.user.username,
    }
    addUserData(request, data)
    segurid=User.groups.through.objects.get(user_id=request.user.id)

    if segurid.group.name == 'Empleado':
        return redirect('/seguridad/login/')
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        if not(M_CLIENTE.objects.filter(ced_ruc__icontains=request.POST['ced_ruc']).exists()):
                            clien = M_CLIENTE()
                            clien.direccion,clien.email,clien.nombre = request.POST['direccion'],request.POST['email'], request.POST['nombre']
                            clien.ced_ruc, clien.telefono, clien.sitioweb = request.POST['ced_ruc'], request.POST['telefono'], request.POST['sitioweb']
                            clien.save()
                        else:
                            messages.error(request, str('Ya se encuentra ese numero de cédula o Ruc'))
                            return redirect('/compra/proveedores/?action=add&id=')

                    if action == 'edit':

                        clien = M_CLIENTE.objects.get(pk=int(request.POST['id']))
                        clien.direccion, clien.email, clien.nombre, clien.sitioweb  = request.POST['direccion'], request.POST['email'],request.POST['nombre'], request.POST['sitioweb']
                        clien.telefono=request.POST['telefono']
                        clien.ced_ruc = request.POST['ced_ruc']
                        clien.save()


                    if action == 'elim':
                        clien = M_CLIENTE.objects.get(pk=int(request.POST['id']))
                        clien.status = False
                        clien.save()

            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/venta/cliente/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:

            if  request.GET['action'] == 'add':
                data['action'] = request.GET['action']
                data['id'] = request.GET['id']

                return render(request, 'venta/cliente_modal.html', data)

            if request.GET['action'] == 'elim':
                clien = M_CLIENTE.objects.get(pk=int(request.GET['id']))
                clien.status = False
                clien.save()
                return redirect('/venta/cliente/')

                '''elif 'imprime' in request.GET:

            cliente = {

                'cliente': M_CLIENTE.objects.filter(status=True).exclude(nombre__icontains='Consumidor Final'), 'empresa': Empresa.objects.first(),
                'model': 'Cliente'
            }
            pdf = render_to_pdf('venta/pdfcliente.html', cliente)
            return HttpResponse(pdf, content_type='application/pdf')'''
            elif (request.GET['action'] == 'edit'):
                data['action'], data['id'] = request.GET['action'], request.GET['id']
                data['client'] = M_CLIENTE.objects.get(id=request.GET['id'])
                return render(request, 'venta/cliente_modal.html', data)
        else:
            # Viaja por get
            data['cliente'] = M_CLIENTE.objects.filter(status=True)
            return render(request, 'venta/cliente.html', data)
