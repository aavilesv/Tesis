from django.urls import path
from venta.view_venta import venta
from venta.view_cliente import cliente
from delivery.views import productos
from delivery.viewcatalogo import catalogo
urlpatterns = [
    path('contactos/' ,venta ,name='contactos'),
    path('cliente/' ,cliente ,name='cliente'),
    path('pedido/' ,productos ,name='productos'),
    path('catalogo/',catalogo ,name='catalogo'),
]