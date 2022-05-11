from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from Tesis.funciones import addUserData, render_to_pdf
from django.db import transaction
from django.shortcuts import render, redirect
from venta.models import M_Producto,M_Marca,M_Ubicacion,M_TipoCategoria
@login_required(login_url='/seguridad/login/')
def articulo(request):
    data ={
        'titulo':'Consulta de Productos',
        'model': 'Artículo',
        'ruta':'/venta/articulo/',
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

                        articulo.m_marca = M_Marca.objects.get(pk=int(request.POST['m_marca']))
                        articulo.nombre, articulo.descripcion = request.POST['nombre'], request.POST['descripcion']
                        articulo.stock, articulo.precio = int(request.POST['stock']), float(request.POST['precio'])
                        articulo.promocion, articulo.stockmin = float(request.POST['promocion']), (
                        request.POST['stockmin'])
                        articulo.stockmax, articulo.m_tipocategoria = int(request.POST['stockmax']), M_TipoCategoria.objects.get(pk=int(request.POST['m_tipocategoria']))
                        articulo.puntoroden, articulo.m_ubicacion = int(request.POST['puntoroden']), M_Ubicacion.objects.get(pk=int(request.POST['m_ubicacion']))

                        if 'image' in request.FILES:
                            articulo.image = request.FILES['image']
                        articulo.save()


                    if action == 'edit':

                        articulo = M_Producto.objects.select_related().get(pk=request.POST['id'])
                        articulo.m_marca = M_Marca.objects.get(pk=int(request.POST['m_marca']))
                        articulo.nombre,articulo.descripcion  = request.POST['nombre'],request.POST['descripcion']
                        articulo.stock,articulo.precio  = int(request.POST['stock']),float(request.POST['precio'])
                        articulo.promocion,articulo.stockmin= float(request.POST['promocion']),(request.POST['stockmin'])
                        articulo.stockmax, articulo.m_tipocategoria = int(request.POST['stockmax']),M_TipoCategoria.objects.get(pk=int(request.POST['m_tipocategoria']))
                        articulo.puntoroden, articulo.m_ubicacion = int(request.POST['puntoroden']), M_Ubicacion.objects.get(pk=int(request.POST['m_ubicacion']))
                        if 'image' in request.FILES:
                            articulo.image = request.FILES['image']

                        articulo.save()

                    if action == 'elim':

                        articul=M_Producto.objects.get(pk=int(request.POST['id']))
                        articul.elim=False
                        articul.save()
            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/venta/articulo/')
    else:
        # Por primera vez viaja por Get

        if 'sucursa' in request.GET:
            if M_Producto.objects.filter(sucursal__id=int(request.GET['sucursa'])).exists():
                data['articulo'],data['buscarid'] = M_Producto.objects.filter(sucursal=3),int(request.GET['sucursa'])

            elif not (M_Producto.objects.filter(sucursal__id=int(request.GET['buscarid'])).exists())  and (int(request.GET['sucursa']) !=0):
                messages.info(request, 'No se hay articulos en esta sucursal')

        elif 'imprime' in request.GET:
            articulos = M_Producto.objects.filter(status=True)
            articulo = {

                'articulo': articulos
            }
            pdf = render_to_pdf('inventario/pdfarticulo.html', articulo)
            return HttpResponse(pdf, content_type='application/pdf')

        elif 'action' in request.GET:
            data['ubicacion'] = M_Ubicacion.objects.filter(status=True)
            data['m_tipocategoria'] = M_TipoCategoria.objects.filter(status=True)
            data['m_marca'] = M_Marca.objects.filter(status=True)
            if (request.GET['action'] == 'add'):
                data['action'], data['id'] = request.GET['action'], request.GET['id']
                return render(request, 'inventario/articulo_modal.html', data)
            if  (request.GET['action'] == 'elim') :
                data['action'], data['id'] = request.GET['action'], request.GET['id']
                producto= M_Producto.objects.get(id=request.GET['id'])
                producto.status=False
                producto.save()
                return redirect('/venta/articulo/')

            if (request.GET['action'] == 'edit'):
                data['action'], data['id'] = request.GET['action'], request.GET['id']


                data['articulo'] = M_Producto.objects.get(id=request.GET['id'])
                return render(request, 'inventario/articulo_modal.html', data)
                #return JsonResponse(data)
            #return JsonResponse(data)

            data['marc']=M_Marca.objects.filter(status=True)
        data['articulo'] = M_Producto.objects.filter(status=True)
        return  render(request, 'inventario/articulo.html', data)
