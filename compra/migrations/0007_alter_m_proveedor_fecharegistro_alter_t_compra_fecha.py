# Generated by Django 4.0.4 on 2022-06-16 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0006_alter_m_proveedor_fecharegistro_alter_t_compra_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_proveedor',
            name='fecharegistro',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 16, 17, 6, 58, 299987)),
        ),
        migrations.AlterField(
            model_name='t_compra',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 16, 17, 6, 58, 299987)),
        ),
    ]