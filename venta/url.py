from django.urls import path
from venta.view_venta import venta
from venta.view_cliente import cliente
from venta.view_articulo import articulo
from venta.view_marca import marca
from venta.viewtipocategoria import  tipocategoria
urlpatterns = [
path('venta/' ,venta ,name='venta'),
path('cliente/' ,cliente ,name='cliente'),
    path('articulo/' ,articulo ,name='articulo'),
path('tipocategoria/' ,tipocategoria ,name='tipocategoria'),
path('marca/' ,marca ,name='marca'),


]