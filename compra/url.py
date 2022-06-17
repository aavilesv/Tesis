from django.urls import path
from compra.views_compra import compra
from compra.view_proveedor import proveedor
from compra.view_reportestock import reportearticulo

urlpatterns = [
    path('compra/' ,compra ,name='compra'),
    path('proveedores/' ,proveedor ,name='proveedor'),
    path('reportearticulo/',reportearticulo,name='reportearticulo'),
]