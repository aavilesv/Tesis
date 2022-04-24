from django.contrib.auth.models import User
from django.db import models
from venta.models import M_Producto
from django.utils import timezone
class M_PROVEEDOR(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="EMPRESA",default='')
    direccion = models.CharField(max_length=200,verbose_name="DIRECCION",default='')
    sitioweb = models.CharField(max_length=200, verbose_name="DIRECCION", default='')
    telefono = models.CharField(max_length=10,verbose_name="TELEFONO",default='')
    fecharegistro = models.DateTimeField(default=timezone.now(), blank=True)
    ced_ruc = models.CharField(max_length=13, verbose_name="Cedula o Ruc",default='')
    email = models.CharField(max_length=200, default="")
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedor'
        ordering = ['nombre']

class T_Compra(models.Model):
    fecha = models.DateTimeField(default=timezone.now(), blank=True)
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal= models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    m_proveedor = models.ForeignKey(M_PROVEEDOR,on_delete=models.PROTECT)

    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'T_Compra'
        verbose_name_plural = 'T_Compra'
        ordering = ['id']





class T_Compradetalle(models.Model):
    t_compra = models.ForeignKey(T_Compra,on_delete=models.PROTECT)
    iva = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    cantidad =models.IntegerField()
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    m_producto= models.ForeignKey(M_Producto, on_delete=models.PROTECT,default=None)
    status = models.BooleanField(default=True)
    class Meta:

        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compra'
        ordering = ['id']

