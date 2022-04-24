# Generated by Django 4.0.4 on 2022-04-18 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('icono', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
                ('orden', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Módulo',
                'verbose_name_plural': 'Módulos',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='ModuloGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('prioridad', models.IntegerField(blank=True, null=True)),
                ('icono', models.CharField(max_length=100)),
                ('grupos', models.ManyToManyField(to='auth.group')),
                ('modulos', models.ManyToManyField(to='Seguridad.modulo')),
            ],
            options={
                'verbose_name': 'Grupo de Módulos',
                'verbose_name_plural': 'Grupos de Módulos',
                'ordering': ('prioridad', 'nombre'),
            },
        ),
    ]
