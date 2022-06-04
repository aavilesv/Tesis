# Generated by Django 4.0.4 on 2022-06-03 20:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0004_alter_m_cliente_fecharegistro_alter_m_producto_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_cliente',
            name='fecharegistro',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 3, 20, 45, 17, 343487), verbose_name='fecha de registro'),
        ),
        migrations.AlterField(
            model_name='m_producto',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 3, 20, 45, 17, 346488)),
        ),
        migrations.AlterField(
            model_name='t_factura',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 3, 20, 45, 17, 347485)),
        ),
    ]
