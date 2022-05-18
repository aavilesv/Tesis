from django.urls import path
from devolucion.views_compra import compra
from devolucion.view_venta import venta
urlpatterns = [
    path('compra/' ,compra ,name='compra'),
    path('venta/' ,venta ,name='proveedor'),
]