from django.contrib import admin

# Register your models here.

from devolucion.models import T_DevolucionCompra,T_DevoluciondetalleCompra,T_DevolucionFactura,T_DevolucionDetalleFactura

admin.site.register(T_DevolucionCompra)
admin.site.register(T_DevoluciondetalleCompra)
admin.site.register(T_DevolucionFactura)
admin.site.register(T_DevolucionDetalleFactura)