from django.db import models
from venta.models import T_Factura
from venta.models import M_Producto
from django.contrib.auth.models import User
from compra.models import T_Compra
from django.utils import timezone

class T_DevolucionFactura(models.Model):
    t_factura = models.ForeignKey(T_Factura, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now(), blank=True)
    motivoanular = models.CharField(max_length=100, blank=True, default=" ")
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    iva = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Devolución de Factura'
        verbose_name_plural = 'Devolución de Factura'
        ordering = ['id']


class T_DevolucionDetalleFactura(models.Model):
    t_devolucionfactura = models.ForeignKey(T_DevolucionFactura,on_delete=models.PROTECT)
    iva = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    cantidad =models.IntegerField()
    cantidaddev = models.IntegerField()
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    m_producto= models.ForeignKey(M_Producto, on_delete=models.PROTECT,default=None)

    class Meta:
        verbose_name = 'Detalle devolucion Factura'
        verbose_name_plural = 'Detalle devolucion Factura'
        ordering = ['id']

class T_DevolucionCompra(models.Model):
    t_compra = models.ForeignKey(T_Compra, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now(), blank=True)
    motivoanular = models.CharField(max_length=100, blank=True, default=" ")
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    iva = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Devolución T_Compra'
        verbose_name_plural = 'Devolución T_Compra'
        ordering = ['id']




class T_DevoluciondetalleCompra(models.Model):
    t_devolucioncompra = models.ForeignKey(T_DevolucionCompra, on_delete=models.PROTECT)
    iva = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    cantidad = models.IntegerField()
    cantidaddev = models.IntegerField()
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    m_producto = models.ForeignKey(M_Producto, on_delete=models.PROTECT, default=None)

    class Meta:
        verbose_name = 'Detalle devolucion compra'
        verbose_name_plural = 'Detalle devolucion compra'
        ordering = ['id']




