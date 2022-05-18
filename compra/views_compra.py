from django.db.models import Q
import datetime
import json
from django.contrib.auth.decorators import login_required
from Tesis.funciones import addUserData, MiPaginador,render_to_pdf
from django.db import transaction, IntegrityError
from django.shortcuts import render,redirect
from venta.models import  M_Producto
from compra.models import  M_PROVEEDOR,T_Compra,T_Compradetalle
from devolucion.models import T_DevolucionCompra,T_DevoluciondetalleCompra
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
@login_required(login_url='/seguridad/login/')
def compra(request):
    data = {
        'titulo': 'CONSULTA DE COMPPRA',
        'model': 'COMPRA',
        'ruta': '/compra/compra/',
        'user': request.user.username,
    }
    addUserData(request, data)
    segurid = User.groups.through.objects.get(user_id=request.user.id)

    if segurid.group.name == 'Empleado':
        return redirect('/seguridad/login/')
    if 'action' in request.GET:
        action = request.GET['action']
        data['action'] = action
        if action == 'cargarcompra':
            try:
                with transaction.atomic():
                    ventajson = json.loads(request.GET['compra'])
                    proveedor = ventajson['cliente']
                    total = ventajson['total']

                    compra = T_Compra()
                    compra.m_proveedor =  M_PROVEEDOR.objects.get(pk=int(proveedor))
                    compra.subtotal = float(ventajson['subtotal'])
                    compra.total=float(total)
                    compra.user=request.user
                    compra.fecha= datetime.datetime.now()
                    compra.save()
                    for item in ventajson['items']:
                        artid = int(item['id']);
                        material =M_Producto.objects.get(pk=artid)

                        detalle = T_Compradetalle()
                        detalle.t_compra=compra
                        detalle.m_producto=material
                        detalle.cantidad=int(item['cantidad'])
                        detalle.total=float(item['precio'])
                        detalle.save()
                        material.stock += int(item['cantidad'])
                        material.save()

                    return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
            except IntegrityError as ex:
                return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                    content_type="application/json")

        if action == 'add':
            data['proveedores'] = M_PROVEEDOR.objects.filter(status=True)
            data['material'] = M_Producto.objects.filter(status=True)
            data['fecha'] = datetime.date.today()
            return render(request, 'compra/compra_form.html', data)
        if action == 'elim':
            compra = T_Compra.objects.get(pk=request.GET['id'])
            compra.status=False
            compra.save()

            for item in T_Compradetalle.objects.filter(t_compra=compra):
                arct = (M_Producto.objects.get(pk=int(item.m_producto.id)))
                arct.stock -= int(item.cantidad)
                arct.save()

            return redirect('/compra/compra/')

        if action == 'ver':
            id = request.GET['id']
            data['compraa'] = T_Compra.objects.get(pk=request.GET['criterio'])
            data['detallee'] = T_Compradetalle.objects.filter(t_compra=data['compraa'])
            return render(request, 'compra/detalle_listado.html', data)
        if action=='devoluci':
            try:
                with transaction.atomic():
                    id = request.GET['id']
                    motivo = request.GET['motivo']
                    compra= T_Compra.objects.get(pk=id)
                    compra.status = False
                    compra.save()
                    devolucion=T_DevolucionCompra()
                    devolucion.t_compra=compra
                    devolucion.fecha=compra.fecha
                    devolucion.motivoanular = motivo
                    devolucion.descuento = compra.descuento
                    devolucion.subtotal = compra.subtotal
                    devolucion.total = compra.total
                    devolucion.user = request.user
                    devolucion.status = compra.status
                    devolucion.save()

                    for item in T_Compradetalle.objects.filter(t_compra=compra):
                        arct = (M_Producto.objects.get(pk=int(item.m_producto.id)))
                        arct.stock += int(item.cantidad)
                        arct.save()
                    for item in T_Compradetalle.objects.filter(t_compra=compra):
                        detalle =T_DevoluciondetalleCompra()
                        detalle.t_devolucioncompra=devolucion
                        detalle.cantidad = item.cantidad
                        detalle.cantidaddev = item.cantidad
                        detalle.subtotal = item.subtotal
                        detalle.total = item.total
                        detalle.m_producto = (M_Producto.objects.get(pk=int(item.m_producto.id)))
                        detalle.save()
                return redirect('/compra/compra/')
            except Exception as ex:
                messages.error(request, str(ex))
    elif 'imprimeunidad' in request.GET:
        id = request.GET['id']
        v = T_Compra.objects.get(pk=int(id))
        t = "0"
        for i in range(9 - len(str(v.id))):
            t += "0"
        compra = {

            'compra': T_Compradetalle.objects.filter(t_compra=T_Compra.objects.get(pk=id)).order_by('m_producto_id'),
            'facturaa': v,
            'model': 'Compra: ' + t + str(v.id)
        }
        pdf = render_to_pdf('compra/pdfcompraunidad.html', compra)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        # Viaja por get cuando hay busqueda con criterio
        criterio = None
        if 'criterio' in request.GET:
            o, p = month_string_to_number(request.GET['criterio'].capitalize())
            criterio = request.GET['criterio'].upper()
        if criterio:
            ba = True
            if criterio.isdigit():
                try:
                    ba = False

                    if T_Compra.objects.filter(fecventa__day=int(criterio)).exists() or T_Compra.objects.filter(
                            fecventa__year=int(criterio)).exists():
                        compras = T_Compra.objects.filter(Q(fecha__day=criterio) | Q(fecha__year=criterio)).order_by(
                            '-fecha')
                except:
                    ba = True
                    compras = T_Compra.objects.filter(status=True).order_by('-fecha')
            if p:
                compras = T_Compra.objects.filter(fecha__month=o).order_by('-fecha')
            elif ba:
                compras = T_Compra.objects.filter( Q(m_proveedor__nombre__contains=criterio) | Q(m_proveedor__ced_ruc__contains=criterio)).order_by('-fecha')




            data['criterio'] = criterio
        else:
            # La primera vez viaje por get sin criterio: consulta todos los datos
            compras = T_Compra.objects.filter(status=True).order_by('-fecha')
        data['compras'] = compras
        # Pagineo
        paging = MiPaginador(compras, 8)
        p = 1
        try:
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)
        except:
            page = paging.page(p)
        data['paging'] = paging
        data['rangospaging'] = paging.rangos_paginado(p)
        data['page'] = page
        data['compras'] = page.object_list
        return render(request, 'compra/compra_listado.html', data)

def month_string_to_number(string):
    m = { "Ener": 1,"Febr": 2,"Marz": 3,"Abri":4,"Mayo":5,"Juni":6,"Juli":7,"Agos":8,"Sept":9,"Octu":10,"Novi":11,"Dici":12}
    s = string.strip()[:4].capitalize()
    try:
        out = m[s]
        return out,True
    except:
        return 0, False