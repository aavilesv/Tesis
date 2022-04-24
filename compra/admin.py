from django.contrib import admin

# Register your models here.

from compra.models import T_Compra,T_Compradetalle,M_PROVEEDOR

admin.site.register(T_Compra)
admin.site.register(T_Compradetalle)
admin.site.register(M_PROVEEDOR)
# Register your models here.