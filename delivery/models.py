from django.contrib.auth.models import User
from django.db import models
from venta.models import M_Producto,M_CLIENTE
from django.utils import timezone

class T_Pedido(models.Model):
    fecha = models.DateTimeField(default=timezone.now(), blank=True)
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    iva = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    m_cliente = models.ForeignKey(M_CLIENTE, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Pedido de Clientes Articulo'
        verbose_name_plural = 'Pedido de Clientes articulos'
        ordering = ['fecha']

class T_Pedidoarticulo(models.Model):

    cantidad = models.IntegerField()
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    m_producto = models.ForeignKey(M_Producto, on_delete=models.PROTECT, default=None)
    pedido = models.ForeignKey(T_Pedido, on_delete=models.PROTECT,default=None)
    class Meta:
        verbose_name = 'Pedido de detalle Articulo'
        verbose_name_plural = 'Pedido de detalle articulos'
        ordering = ['id']

