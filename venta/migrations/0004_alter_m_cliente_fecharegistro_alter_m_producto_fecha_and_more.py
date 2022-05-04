# Generated by Django 4.0.4 on 2022-05-04 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_alter_m_cliente_fecharegistro_alter_m_producto_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_cliente',
            name='fecharegistro',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 4, 17, 14, 26, 51797), verbose_name='fecha de registro'),
        ),
        migrations.AlterField(
            model_name='m_producto',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 4, 17, 14, 26, 53797)),
        ),
        migrations.AlterField(
            model_name='m_producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='m_producto',
            name='promocion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='t_factura',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 4, 17, 14, 26, 53797)),
        ),
    ]
