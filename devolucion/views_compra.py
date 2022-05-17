from django.db.models import Q
import datetime
import json
from django.contrib.auth.decorators import login_required
from Tesis.funciones import addUserData, MiPaginador
from django.db import transaction, IntegrityError
from django.shortcuts import render,redirect
from venta.models import  M_Producto
from compra.models import  M_PROVEEDOR,T_Compra,T_Compradetalle
from django.http import HttpResponse
from django.contrib.auth.models import User
@login_required(login_url='/seguridad/login/')
def compra(request):
    data = {
        'titulo': 'CONSULTA DE COMPPRA',
        'model': 'COMPRA',
        'ruta': '/devolucioncompras/compra/',
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
            return render(request, 'devolucioncompras/compra_form.html', data)
        if action == 'elim':
            compra = T_Compra.objects.get(pk=request.GET['id'])
            compra.status=False
            compra.save()
            return redirect('/devolucioncompras/compra/')

        if action == 'ver':
            id = request.GET['id']
            data['compraa'] = T_Compra.objects.get(pk=request.GET['criterio'])
            data['detallee'] = T_Compradetalle.objects.filter(t_compra=data['compraa'])
            return render(request, 'devolucioncompras/detalle_listado.html', data)
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
        return render(request, 'devolucioncompras/compra_listado.html', data)

def month_string_to_number(string):
    m = { "Ener": 1,"Febr": 2,"Marz": 3,"Abri":4,"Mayo":5,"Juni":6,"Juli":7,"Agos":8,"Sept":9,"Octu":10,"Novi":11,"Dici":12}
    s = string.strip()[:4].capitalize()
    try:
        out = m[s]
        return out,True
    except:
        return 0, False