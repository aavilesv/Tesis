# Generated by Django 4.0.4 on 2022-04-24 20:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devolucion', '0002_alter_t_devolucioncompra_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_devolucioncompra',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 24, 20, 29, 4, 670165)),
        ),
        migrations.AlterField(
            model_name='t_devolucionfactura',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 24, 20, 29, 4, 669166)),
        ),
    ]
