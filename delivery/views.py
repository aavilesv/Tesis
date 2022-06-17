from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from Tesis.funciones import addUserData, render_to_pdf
import json
from django.utils import timezone
from delivery.models import T_Pedido, T_Pedidoarticulo
from venta.models import M_Producto, M_Marca, M_Ubicacion, M_TipoCategoria, T_Factura
from django.db import transaction, IntegrityError

from django.shortcuts import render,redirect
@login_required(login_url='/seguridad/login/')
def productos(request):
    data ={
        'titulo':'Consulta de Pedidos',
        'model': 'Pedidos',
        'ruta':'/delivery/pedido/',
        'user': request.user.username,
    }
    addUserData(request, data)
    # Por primera vez viaja por Get

    if 'sucursa' in request.GET:
        if M_Producto.objects.filter(sucursal__id=int(request.GET['sucursa'])).exists():
            data['articulo'],data['buscarid'] = M_Producto.objects.filter(sucursal=3),int(request.GET['sucursa'])

        elif not (M_Producto.objects.filter(sucursal__id=int(request.GET['buscarid'])).exists())  and (int(request.GET['sucursa']) !=0):
            messages.info(request, 'No se hay articulos en esta sucursal')
    elif 'imprimeunidad' in request.GET:
        id = request.GET['id']
        v = T_Pedido.objects.get(pk=int(id))
        t = "0"
        for i in range(9 - len(str(v.id))):
            t += "0"
        pedido = {

            'detallepedido': T_Pedidoarticulo.objects.filter(pedido=T_Pedido.objects.get(pk=id)).order_by('m_producto_id'),
            'pedido': v,
            'model': 'Pedido: ' + t + str(v.id)
        }
        pdf = render_to_pdf('delivery/pedidopdf.html', pedido)
        return HttpResponse(pdf, content_type='application/pdf')
    elif 'imprime' in request.GET:
        articulos = M_Producto.objects.filter(status=True)
        articulo = {

            'articulo': articulos
        }
        pdf = render_to_pdf('inventario/pdfarticulo.html', articulo)
        return HttpResponse(pdf, content_type='application/pdf')

    elif 'action' in request.GET:
        action = request.GET['action']
        data['action'] = action
        if action == 'facturar':
            if T_Pedido.objects.filter(status=False,user=request.user).exists():
                data['venta'] = T_Factura.objects.filter(status=True,pedido=request.user.id).order_by('-fecha')
                return render(request, 'delivery/listadodepedidofactura.html', data)
            messages.error(request, str('Todavía no se realiza factura de su pedido'))
            return redirect('/delivery/pedido/')
        if action == 'pedidocomprar':
            try:
                with transaction.atomic():
                    pedidojson = json.loads(request.GET['pedido'])
                    pedido = T_Pedido()
                    pedido.fecha=timezone.now()
                    pedido.descuento = 0
                    pedido.subtotal = float(request.GET['subtotal'])
                    pedido.iva = 0
                    pedido.total = float(request.GET['total'])
                    pedido.user = request.user
                    pedido.status = True
                    pedido.save()
                    for item in pedidojson:
                        detallepedido =T_Pedidoarticulo()
                        detallepedido.cantidad=int(item['cantidad'])
                        detallepedido.descuento =0
                        detallepedido.subtotal = float(item['precio'])
                        detallepedido.total = float(item['total'])
                        detallepedido.m_producto = M_Producto.objects.get(pk=int(item['id']))
                        detallepedido.pedido = pedido
                        detallepedido.save()



                    return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
            except IntegrityError as ex:
                return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                    content_type="application/json")
        if action =='listadopedido':
            data['pedido'] = T_Pedido.objects.filter(status=True).order_by('-fecha')
            return  render(request, 'delivery/listadopedidos.html', data)


    #data['articulo'] = M_Producto.objects.filter(status=True)
    data['pedido'] = T_Pedido.objects.filter(status=True).order_by('-fecha')
    return  render(request, 'delivery/listadopedidos.html', data)
