from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class M_CLIENTE(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre",default='')
    direccion = models.CharField(max_length=200,verbose_name="DIRECCION",default='')
    sitioweb = models.CharField(max_length=200, verbose_name="sitio web", default='')
    telefono = models.CharField(max_length=10,verbose_name="TELEFONO",default='')
    ced_ruc = models.CharField(max_length=13, verbose_name="Cedula o Ruc",default='')
    fecharegistro = models.DateTimeField(default=timezone.now(), verbose_name="fecha de registro", blank=True)
    email = models.CharField(max_length=200,verbose_name="Email", default="")
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Cliente'
        ordering = ['id']

class M_TipoCategoria(models.Model):
    descripcion=models.CharField(max_length=100, verbose_name="Descripción",blank=True,default=" ")
    status=models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.descripcion)
    class Meta:
        verbose_name = 'Tipo Categoria'
        verbose_name_plural = 'Tipo Categorias'
        ordering = ['descripcion']

class M_Marca(models.Model):
    nombre=models.CharField(max_length=100, verbose_name="Nombre",blank=True,default=" ")
    status=models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.nombre)
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']

class M_Ubicacion(models.Model):
    descripcion=models.CharField(max_length=100, verbose_name="Descripción",blank=True,default=" ")
    status=models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.descripcion)
    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['descripcion']

class M_Producto(models.Model):
    m_ubicacion = models.ForeignKey(M_Ubicacion, blank=True, null=True, on_delete=models.PROTECT)
    m_marca = models.ForeignKey(M_Marca, blank=True, null=True, on_delete=models.PROTECT)
    m_tipocategoria=models.ForeignKey(M_TipoCategoria, blank=True, null=True, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=200, default=" ")
    nombre = models.CharField(max_length=200, default=" ")
    precio = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    stock= models.IntegerField(default=0)
    stockmin = models.IntegerField(default=0)
    stockmax = models.IntegerField(default=0)
    image = models.ImageField(upload_to='articulo/%Y/%m/%d/', default='')
    promocion = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    fecha = models.DateTimeField(default=timezone.now(), blank=True)
    puntoroden = models.IntegerField(default=0)
    iva = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return '{}-{}'.format(self.nombre,self.descripcion)
    class Meta:
        verbose_name = 'M_Producto'
        verbose_name_plural = 'M_Productos'
        ordering = ['id']

class T_Factura(models.Model):
    fecha = models.DateTimeField(default=timezone.now(), blank=True)
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal= models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    m_cliente = models.ForeignKey(M_CLIENTE,on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'T_Factura'
        verbose_name_plural = 'T_Factura'
        ordering = ['id']

class T_Facturadetalle(models.Model):
    t_factura = models.ForeignKey(T_Factura,on_delete=models.PROTECT)
    iva = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    cantidad =models.IntegerField()
    descuento = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=19,default=0)
    m_producto= models.ForeignKey(M_Producto, on_delete=models.PROTECT,default=None)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}-{}-{}-{}'.format(self.t_factura.id, self.id,self.cantidad,self.m_producto.nombre,self.m_producto.descripcion)

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalle de Factura'
        ordering = ['id']


