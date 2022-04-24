from django.contrib import admin

# Register your models here.

from venta.models import T_Factura,T_Facturadetalle,M_Producto,M_Marca,M_Ubicacion,M_TipoCategoria,M_CLIENTE

admin.site.register(T_Factura)
admin.site.register(T_Facturadetalle)
admin.site.register(M_Producto)
admin.site.register(M_Marca)
admin.site.register(M_Ubicacion)
admin.site.register(M_TipoCategoria)
admin.site.register(M_CLIENTE)
# Register your models here.