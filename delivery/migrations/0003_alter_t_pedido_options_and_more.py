# Generated by Django 4.0.4 on 2022-06-16 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_alter_t_pedido_fecha'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='t_pedido',
            options={'verbose_name': 'Pedido de Clientes Articulo', 'verbose_name_plural': 'Pedido de Clientes articulos'},
        ),
        migrations.AlterModelOptions(
            name='t_pedidoarticulo',
            options={'ordering': ['-id'], 'verbose_name': 'Pedido de detalle Articulo', 'verbose_name_plural': 'Pedido de detalle articulos'},
        ),
        migrations.RemoveField(
            model_name='t_pedido',
            name='m_cliente',
        ),
        migrations.AlterField(
            model_name='t_pedido',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 16, 17, 6, 58, 306983)),
        ),
    ]
