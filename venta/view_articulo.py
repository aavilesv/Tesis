from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from Tesis.funciones import addUserData, render_to_pdf
from django.db import transaction
from django.shortcuts import render, redirect
from venta.models import M_Producto,M_Marca,M_Ubicacion,M_TipoCategoria
@login_required(login_url='/seguridad/login/')
def articulo(request):
    data ={
        'titulo':'Consulta de artículos -FULL AUTO MILAGRO',
        'model': 'Artículo',
        'ruta':'/inventario/articulo/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        articulo =M_Producto()

                        articulo.marca, articulo.image  = M_Marca.objects.get(pk=int(request.POST['marca'])), request.FILES['image']
                        articulo.nombre,articulo.descripcion  = request.POST['nombre'],request.POST['descripcion']
                        articulo.stock,articulo.iva,articulo.precio  = int(request.POST['stock']), float(request.POST['iva']),float(request.POST['precio'])
                        articulo.descuento,articulo.subtotal= float(request.POST['descuento']),float(request.POST['subtotal'])
                        if not 'status' in request.POST:
                            articulo.status =False
                        articulo.save()

                    if action == 'edit':

                        articulo = M_Producto.objects.select_related().get(pk=request.POST['id'])
                        articulo.marca = M_Marca.objects.get(pk=int(request.POST['marca']))
                        articulo.nombre,articulo.descripcion  = request.POST['nombre'],request.POST['descripcion']
                        articulo.stock,articulo.iva,articulo.precio  = int(request.POST['stock']), float(request.POST['iva']),float(request.POST['precio'])
                        articulo.descuento,articulo.subtotal= float(request.POST['descuento']),float(request.POST['subtotal'])
                        if 'image' in request.FILES:
                            articulo.image = request.FILES['image']
                        if not 'status' in request.POST:
                            articulo.status = False
                        if 'status' in request.POST:
                            articulo.status = True
                        articulo.save()

                    if action == 'elim':

                        articul=M_Producto.objects.get(pk=int(request.POST['id']))
                        articul.elim=False
                        articul.save()
            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/inventario/articulo/')
    else:
        # Por primera vez viaja por Get
        data['articulo'],data['buscarid'] = M_Producto.objects.filter(status=True),0
        if 'sucursa' in request.GET:
            if M_Producto.objects.filter(sucursal__id=int(request.GET['sucursa'])).exists():
                data['articulo'],data['buscarid'] = M_Producto.objects.filter(sucursal=3),int(request.GET['sucursa'])

            elif not (M_Producto.objects.filter(sucursal__id=int(request.GET['buscarid'])).exists())  and (int(request.GET['sucursa']) !=0):
                messages.info(request, 'No se hay articulos en esta sucursal')

        elif 'imprime' in request.GET:
            if 'buscarid' in request.GET:
                if M_Producto.objects.filter(sucursal__id=int(request.GET['buscarid'])).exists():
                    articulos = M_Producto.objects.filter(sucursal=3,elim=True)
                    articulo = {

                        'articulo': articulos
                    }
                    pdf = render_to_pdf('inventario/pdfarticulo.html', articulo)
                    return HttpResponse(pdf, content_type='application/pdf')
                elif int(request.GET['buscarid']) == 0:
                    articulos = M_Producto.objects.filter(elim=True)

                    articulo = {

                        'articulo': articulos
                    }
                    pdf = render_to_pdf('inventario/pdfarticulo.html', articulo)
                    return HttpResponse(pdf, content_type='application/pdf')

        elif 'action' in request.GET:
            data['action'] = request.GET['action']
            if not (request.GET['action'] == 'add') :
                data['id'] = request.GET['id']
                data['articulo']= M_Producto.objects.get(pk=int(request.GET['id']))
            data['marc']=M_Marca.objects.filter(status=True)
            return render(request, 'inventario/articulo_modal.html', data)

        return render(request, 'inventario/articulo.html', data)
