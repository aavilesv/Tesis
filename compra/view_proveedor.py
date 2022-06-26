from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from compra.models import M_PROVEEDOR

from Tesis.funciones import addUserData
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

@login_required(login_url='/seguridad/login/')
def proveedor(request):
    data ={
        'titulo':'Consulta de proveedores -FULL AUTO MILAGRO',
        'model': 'Proveedor',
        'ruta':'/compra/proveedores/',
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
                        if not(M_PROVEEDOR.objects.filter(ced_ruc__icontains=request.POST['ced_ruc']).exists()):
                            proveedo = M_PROVEEDOR()
                            proveedo.direccion = request.POST['direccion']
                            proveedo.email = request.POST['email']
                            proveedo.nombre = request.POST['nombre']
                            proveedo.ced_ruc = request.POST['ced_ruc']
                            proveedo.telefono = request.POST['telefono']
                            proveedo.sitioweb = request.POST['sitioweb']
                            proveedo.save()
                        else:
                            messages.error(request, str('Ya se encuentra ese numero de cédula o Ruc'))
                            return redirect('/compra/proveedores/?action=add&id=')




                    if action == 'edit':

                        proveedo = M_PROVEEDOR.objects.get(pk=int(request.POST['id']))
                        proveedo.direccion = request.POST['direccion']
                        proveedo.email = request.POST['email']
                        proveedo.nombre = request.POST['nombre']
                        proveedo.ced_ruc = request.POST['ced_ruc']
                        proveedo.telefono = request.POST['telefono']
                        proveedo.sitioweb= request.POST['sitioweb']


                        proveedo.save()


            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/compra/proveedores/')
    else:
        if 'action' in request.GET:

            if request.GET['action'] == 'add':
                data['action'] = request.GET['action']
                data['id'] = request.GET['id']

                return render(request, 'compra/proveedor_modal.html', data)

            if request.GET['action'] == 'elim':
                clien = M_PROVEEDOR.objects.get(pk=int(request.GET['id']))
                clien.status = False
                clien.save()
                return redirect('/compra/proveedores/')

                '''elif 'imprime' in request.GET:

            cliente = {

                'cliente': M_CLIENTE.objects.filter(status=True).exclude(nombre__icontains='Consumidor Final'), 'empresa': Empresa.objects.first(),
                'model': 'Cliente'
            }
            pdf = render_to_pdf('venta/pdfcliente.html', cliente)
            return HttpResponse(pdf, content_type='application/pdf')'''
            elif (request.GET['action'] == 'edit'):
                data['action'], data['id'] = request.GET['action'], request.GET['id']
                data['proveedor'] = M_PROVEEDOR.objects.get(id=request.GET['id'])
                return render(request, 'compra/proveedor_modal.html', data)

        else:
            # Viaja por get
            proveedor = M_PROVEEDOR.objects.filter(status=True)
            data['proveedor'] = proveedor
            return render(request, 'compra/Proveedor.html', data)
