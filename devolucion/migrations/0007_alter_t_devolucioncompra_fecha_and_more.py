# Generated by Django 4.0.4 on 2022-06-16 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devolucion', '0006_alter_t_devolucioncompra_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_devolucioncompra',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 16, 17, 6, 58, 303986)),
        ),
        migrations.AlterField(
            model_name='t_devolucionfactura',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 16, 17, 6, 58, 302986)),
        ),
    ]
