from django.contrib.auth.models import User
from django.db.models import Q
from venta.models import M_Producto
from Tesis.funciones import addUserData, render_to_pdf
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction ,IntegrityError
from django.utils.html import strip_tags
import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from venta.models import T_Factura,T_Facturadetalle,M_Producto,M_CLIENTE
@login_required(login_url='/seguridad/login/')
def venta(request):
    data ={
        'titulo':'Consulta de ventas -FULL AUTO MILAGRO',
        'model': 'Venta',
        'ruta':'/venta/venta/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if 'action' in request.GET:
        action = request.GET['action']
        data['action'] = action
        if action == 'cargaventa':
            try:
                with transaction.atomic():
                    ventajson = json.loads(request.GET['venta'])

                    vent = T_Factura()
                    vent.m_cliente = M_CLIENTE.objects.get(pk=int(ventajson['cliente']))
                    vent.subtotal ,vent.total  = round(float(ventajson['subtotal'])), round(float(ventajson['total']))
                    vent.fecha,vent.descuento = datetime.datetime.now(),0
                    vent.user = (request.user)
                    vent.save()

                    for item in ventajson['items']:

                        if M_Producto.objects.filter(id=int(item['id'])).exists():
                            detalle = T_Facturadetalle()
                            detalle.t_factura,detalle.m_producto = vent, M_Producto.objects.get(pk=int(item['id']))
                            detalle.cantidad,detalle.total  =int(item['cantidad']), float(item['precio'])
                            arct = M_Producto.objects.get(pk=int(item['id']))
                            arct.stock -= int(item['cantidad'])
                            arct.save()
                            detalle.preciototal = round(float(item['precio'])*int(item['cantidad']))
                            detalle.save()
                    # asunto = 'Compra en Taller Herrera'
                    # email_from = settings.EMAIL_HOST_USER
                    # data['detalle'] = Detallecompra.objects.filter(factura=facturar)
                    # data['empresa'] = Empresa.objects.get(user=request.user)
                    # email_to = [cliente.email]
                    # datos = {
                    #     'factura': facturar,
                    #     'detalle': Detallecompra.objects.filter(factura=facturar),
                    #     'sucursal': Empresa.objects.get(user=request.user),
                    # }
                    # html_message = render_to_string('facturacion/correoenvio.html', datos)
                    # plain_message = strip_tags(html_message)
                    # send_mail(asunto, plain_message, email_from, email_to, html_message=html_message,
                    #           fail_silently=True)
                    return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
            except IntegrityError as ex:

                return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                    content_type="application/json")
        if action == 'add':

            data['cliente'] = M_CLIENTE.objects.filter(status=True)
            data['articul'] = M_Producto.objects.filter(status=True)
            data['fecha'] = datetime.date.today()
            return render(request, 'venta/venta_form.html', data)

            if action == 'ver':
                id = request.GET['id']
                v=T_Factura.objects.get(pk=id)
                data['venta'],data['detalle'] =v,T_Facturadetalle.objects.filter(venta=T_Factura.objects.get(pk=id)).order_by('articulo_id')

                return render(request, 'venta/venta_visualizar.html', data)
        if action == 'elim':
            venta = T_Factura.objects.get(pk=request.GET['id'])
            venta.status = False
            venta.save()
            for item in T_Facturadetalle.objects.filter(t_factura=venta):
                arct = (M_Producto.objects.get(pk=int(item.m_producto.id)))
                arct.stock += int(item.cantidad)
                arct.save()
            return redirect('/venta/venta/')

    elif 'imprimeunidad' in request.GET:
        id = request.GET['id']
        v=T_Factura.objects.get(pk=int(id))
        t = "0"

        factura = {

            'venta': T_Facturadetalle.objects.filter(t_factura=T_Factura.objects.get(pk=id)).order_by('m_producto_id'),
            'facturaa':v,
            'model': 'Factura: '+t+str(v.id)
        }
        pdf = render_to_pdf('venta/pdffacturaunidad.html', factura)
        return HttpResponse(pdf, content_type='application/pdf')

    elif 'imprime' in request.GET:

        cliente = {

            'venta': T_Factura.objects.all(),
            'model': 'Factura'
        }
        pdf = render_to_pdf('venta/pdfventa.html', cliente)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        # Viaja por get
        data['venta'] =  T_Factura.objects.filter(status=True).order_by('id')
        return render(request, 'venta/Venta.html', data)
