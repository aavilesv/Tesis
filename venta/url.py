from django.urls import path
from venta.view_venta import venta
from venta.view_cliente import cliente
from venta.view_articulo import articulo
from venta.view_marca import marca
urlpatterns = [
path('venta/' ,venta ,name='venta'),
path('cliente/' ,cliente ,name='cliente'),
    path('articulo/' ,articulo ,name='articulo'),
path('marca/' ,marca ,name='marca'),


]