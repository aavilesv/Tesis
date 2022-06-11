from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from Tesis.funciones import addUserData, render_to_pdf
from django.db import transaction
from django.shortcuts import render, redirect
from venta.models import M_Marca, M_TipoCategoria,M_Ubicacion


@login_required(login_url='/seguridad/login/')
def ubicacion(request):
    data ={
        'titulo':'Consulta de Ubicación',
        'model': 'Ubicación',
        'ruta':'/venta/ubicacion/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        marca = M_Ubicacion()
                        marca.descripcion = request.POST['nombre']
                        staa = True
                        if not 'status' in request.POST:
                            staa = False
                        marca.status = staa
                        marca.save()
                    if action == 'edit':
                        marca = M_Ubicacion.objects.select_related().get(pk=request.POST['id'])
                        marca.descripcion= request.POST['nombre']
                        staa = True
                        if not 'status' in request.POST:
                            staa = False
                        marca.status = staa
                        marca.save()

            except Exception as ex:
                messages.error(request, 'Error, dato ya registrado')
            return redirect('/venta/ubicacion/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit':
                data['id'] = request.GET['id']
                data['marca']=M_Ubicacion.objects.get(pk=int(request.GET['id']))
                return render(request, 'inventario/ubacion_from.html', data)
            if action == 'add':
                data['id'] = request.GET['id']

                return render(request, 'inventario/ubacion_from.html', data)
            if action == 'elim':
                id = request.GET['id']
                marca = M_Ubicacion.objects.get(pk=int(id))
                marca.elim = False
                marca.save()
                return redirect('/venta/ubicacion/')
        elif 'imprime' in request.GET:

            marca = {

                'marca': M_Ubicacion.objects.filter(status=True),
                'model': 'Marca'
            }
            pdf = render_to_pdf('inventario/pdfmarca.html', marca)
            return HttpResponse(pdf, content_type='application/pdf')


        else:
            # Viaja por get
            data['marca']=M_Ubicacion.objects.all()
            return render(request, 'inventario/ubicación.html', data)
